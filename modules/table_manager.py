import sqlite3
from tkinter import messagebox

class TableManager:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, table_name, columns):
        """ Crea una tabla en la base de datos con las columnas especificadas. """
        cursor = self.conn.cursor()
        columns_definition = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
        self.conn.commit()
        print(f"Tabla '{table_name}' creada con columnas: {', '.join(columns.keys())}.")

    def list_tables(self):
        """ Devuelve una lista de los nombres de las tablas en la base de datos. """
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]
    
    # Nota: La función create_or_connect_db no debería estar en este módulo



