import pandas as pd
import re

def formatar_cpf(cpf):

    cpf = re.sub(r"\D", "", str(cpf))

    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def transform():

    transacoes = pd.read_csv(
        "/opt/airflow/data/transacoes_nogtech.csv",
        sep=";",
        encoding="latin1"
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
            transacoes["data_transacao"]
        ).dt.strftime("%Y-%m")
    )

    resultado = transacoes.merge(
        engajamento,
        on=["cpf_aluno", "mes_referencia"],
        how="left"
    )

    resultado.to_csv(
        "/opt/airflow/data/resultado.csv",
        index=False
    )