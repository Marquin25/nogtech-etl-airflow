import pandas as pd
from sqlalchemy import create_engine

def load():

    df = pd.read_csv("/opt/airflow/data/resultado.csv")

    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres:5432/nogtech"
    )

    df.to_sql(
        "fato_vendas",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Carga concluída: {len(df)} registros gravados em fato_vendas")
