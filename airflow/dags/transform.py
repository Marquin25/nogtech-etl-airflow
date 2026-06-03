import pandas as pd
import re

def formatar_cpf(cpf):
    cpf = re.sub(r"\D", "", str(cpf))
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def anonimizar_cpf(cpf):
    return f"***.{cpf[4:7]}.{cpf[8:11]}-**"

def transform():

    transacoes = pd.read_csv(
        "/opt/airflow/data/transacoes_nogtech.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    engajamento = pd.read_json(
        "/opt/airflow/data/engajamento_alunos.json"
    )

    transacoes["cpf_aluno"] = transacoes["cpf_aluno"].apply(formatar_cpf)
    engajamento["cpf_aluno"] = engajamento["cpf_aluno"].apply(formatar_cpf)

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

    # LGPD
    resultado["cpf_aluno"] = resultado["cpf_aluno"].apply(anonimizar_cpf)

    if "nome_aluno" in resultado.columns:
        resultado.drop(columns=["nome_aluno"], inplace=True)

    resultado.to_csv(
        "/opt/airflow/data/resultado.csv",
        index=False
    )