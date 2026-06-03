import pandas as pd
import re
import requests


def formatar_cpf(cpf):
    cpf = re.sub(r"\D", "", str(cpf))
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def anonimizar_cpf(cpf):
    return f"***.{cpf[4:7]}.{cpf[8:11]}-**"


def buscar_feriados(ano):

    url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        return {feriado["date"] for feriado in resposta.json()}

    return set()


def buscar_cep(cep, cache):

    cep = str(int(float(cep))) if pd.notna(cep) else ""

    if cep in cache:
        return cache[cep]

    url = f"https://brasilapi.com.br/api/cep/v2/{cep}"

    try:

        resposta = requests.get(
            url,
            timeout=5
        )

        if resposta.status_code == 200:

            dados = resposta.json()

            resultado = {
                "cidade": dados.get("city"),
                "uf": dados.get("state"),
                "bairro": dados.get("neighborhood")
            }

            cache[cep] = resultado

            return resultado

    except Exception:
        pass

    return {
        "cidade": None,
        "uf": None,
        "bairro": None
    }


def transform():

    transacoes = pd.read_csv(
        "/opt/airflow/data/transacoes_nogtech.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    engajamento = pd.read_json(
        "/opt/airflow/data/engajamento_alunos.json"
    )

    transacoes["cpf_aluno"] = (
        transacoes["cpf_aluno"]
        .apply(formatar_cpf)
    )

    engajamento["cpf_aluno"] = (
        engajamento["cpf_aluno"]
        .apply(formatar_cpf)
    )

    transacoes["mes_referencia"] = (
        pd.to_datetime(
            transacoes["data_transacao"],
            format="mixed",
            dayfirst=True
        ).dt.strftime("%Y-%m")
    )

    resultado = transacoes.merge(
        engajamento,
        on=["cpf_aluno", "mes_referencia"],
        how="left"
    )

    # Feriados
    feriados_2024 = buscar_feriados(2024)

    resultado["data_transacao"] = pd.to_datetime(
        resultado["data_transacao"],
        format="mixed",
        dayfirst=True
    )

    resultado["venda_em_feriado"] = (
        resultado["data_transacao"]
        .dt.strftime("%Y-%m-%d")
        .isin(feriados_2024)
    )

    # CEP + Cache
    cache_cep = {}

    for cep in resultado["cep_cobranca"].dropna().unique():
        buscar_cep(cep, cache_cep)

    resultado["cidade"] = (
        resultado["cep_cobranca"]
        .apply(
            lambda cep: cache_cep.get(
                str(int(float(cep))),
                {}
            ).get("cidade")
            if pd.notna(cep)
            else None
        )
    )

    resultado["uf"] = (
        resultado["cep_cobranca"]
        .apply(
            lambda cep: cache_cep.get(
                str(int(float(cep))),
                {}
            ).get("uf")
            if pd.notna(cep)
            else None
        )
    )

    resultado["bairro"] = (
        resultado["cep_cobranca"]
        .apply(
            lambda cep: cache_cep.get(
                str(int(float(cep))),
                {}
            ).get("bairro")
            if pd.notna(cep)
            else None
        )
    )

    # LGPD
    resultado["cpf_aluno"] = (
        resultado["cpf_aluno"]
        .apply(anonimizar_cpf)
    )

    if "nome_aluno" in resultado.columns:
        resultado.drop(
            columns=["nome_aluno"],
            inplace=True
        )

    resultado.to_csv(
        "/opt/airflow/data/resultado.csv",
        index=False
    )