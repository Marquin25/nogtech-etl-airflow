import pandas as pd
from sqlalchemy import create_engine, text

def load():

    df = pd.read_csv("/opt/airflow/data/resultado.csv")

    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres:5432/nogtech"
    )

    with engine.connect() as conn:
        tabela_existe = conn.execute(text(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'fato_vendas')"
        )).scalar()

        if tabela_existe and not df.empty:
            datas = df["data_transacao"].unique().tolist()
            datas_str = ", ".join([f"'{d}'" for d in datas])
            conn.execute(text(
                f"DELETE FROM fato_vendas WHERE data_transacao IN ({datas_str})"
            ))
            conn.commit()

    df.to_sql(
        "fato_vendas",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Carga concluída: {len(df)} registros gravados em fato_vendas")
