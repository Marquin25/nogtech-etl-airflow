import pandas as pd

def extract():

    transacoes = pd.read_csv(
        "/opt/airflow/data/transacoes_nogtech.csv",
        sep=";",
        encoding="latin1"
    )

    engajamento = pd.read_json(
        "/opt/airflow/data/engajamento_alunos.json"
    )

    print(transacoes.head())
    print(engajamento.head())