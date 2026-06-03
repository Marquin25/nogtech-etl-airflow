import pandas as pd
from sqlalchemy import create_engine

def load():

    df = pd.read_csv("/opt/airflow/data/resultado.csv")

    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres:5432/nogtech"
    )

    df.to_sql(
        "alunos_tratados",
        engine,
        if_exists="replace",
        index=False
    )

    print("Dados carregados com sucesso!")