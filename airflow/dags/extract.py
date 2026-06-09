import pandas as pd

def extract():

    transacoes = pd.read_csv(
        "/opt/airflow/data/transacoes_nogtech.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    engajamento = pd.read_json(
        "/opt/airflow/data/engajamento_alunos.json"
    )

    transacoes["mes_referencia"] = pd.to_datetime(
    transacoes["data_transacao"],
    format="mixed",
    dayfirst=True
).dt.strftime("%Y-%m")

    engajamento["mes_referencia"] = engajamento["mes_referencia"].astype(str)

    resultado = transacoes.merge(
        engajamento,
        on=["cpf_aluno", "mes_referencia"],
        how="left"
    )

    resultado.to_csv(
        "/opt/airflow/data/resultado.csv",
        index=False
    )

    print(f"Extração concluída: {len(resultado)} registros")
