import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root@localhost:3306/project', echo=False)

def run_sql_query(sql: str) -> pd.DataFrame:
    try:
        with engine.connect() as conn:
            sql_lower = sql.strip().lower()
            if sql_lower.startswith(("insert", "update", "delete")):
                conn.execute(text(sql))
                conn.commit()
                return pd.DataFrame()
            else:
                df = pd.read_sql(sql, con=conn)
                return df
    except Exception as e:
        raise RuntimeError(f"Failed to execute SQL: {e}")
