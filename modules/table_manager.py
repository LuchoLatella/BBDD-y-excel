import sqlite3
from tkinter import messagebox

class TableManager:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, table_name, columns):
        """ Crea una tabla en la base de datos con las columnas especificadas. """
        try:
            cursor = self.conn.cursor()
            columns_definition = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
            self.conn.commit()
            print(f"Tabla '{table_name}' creada con columnas: {', '.join(columns.keys())}.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {str(e)}")

    def list_tables(self):
        """ Devuelve una lista de los nombres de las tablas en la base de datos. """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [table[0] for table in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al listar las tablas: {str(e)}")
            return []

    def create_index(self, table_name, column_name):
        """ Crea un índice en la columna especificada de la tabla. """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE INDEX idx_{column_name} ON {table_name}({column_name})")
            self.conn.commit()
            print(f"Index created on column '{column_name}' in table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error al crear el índice: {str(e)}")

    def create_foreign_key(self, table_name, column_name, ref_table, ref_column):
        """ Crea una clave foránea en la tabla especificada. """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name}_ref INTEGER, "
                           f"FOREIGN KEY ({column_name}_ref) REFERENCES {ref_table}({ref_column})")
            self.conn.commit()
            print(f"Foreign key created in '{table_name}' referencing '{ref_table}({ref_column})'.")
        except sqlite3.Error as e:
            print(f"Error al crear la clave foránea: {str(e)}")



