import sqlite3
import pandas as pd

DB_NAME = 'mi_base_de_datos.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def save_dataframe_to_db(df, table_name):
    conn = connect_db()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def load_dataframe_from_db(table_name):
    conn = connect_db()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def get_columns(table_name):
    conn = connect_db()
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 1", conn)
    conn.close()
    return df.columns
