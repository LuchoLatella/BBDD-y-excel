import mysql.connector
from mysql.connector import Error

class TableManager:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, table_name, columns):
        """ Crea una tabla en la base de datos con las columnas especificadas. """
        cursor = self.conn.cursor()
        columns_definition = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
            self.conn.commit()
            print(f"Tabla '{table_name}' creada con columnas: {', '.join(columns.keys())}.")
        except Error as e:
            print(f"Error al crear la tabla '{table_name}': {e}")

    def list_tables(self):
        """ Devuelve una lista de los nombres de las tablas en la base de datos. """
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES;")
        return [table[0] for table in cursor.fetchall()]

    def create_index(self, table_name, column_name):
        """ Crea un índice en una columna especificada. """
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"CREATE INDEX idx_{column_name} ON {table_name}({column_name})")
            self.conn.commit()
            print(f"Índice creado en la columna '{column_name}' en la tabla '{table_name}'.")
        except Error as e:
            print(f"Error al crear el índice: {e}")

    def create_foreign_key(self, table_name, column_name, ref_table, ref_column):
        """ Crea una clave foránea en la tabla especificada. """
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name}_ref INT, "
                           f"ADD CONSTRAINT fk_{column_name} FOREIGN KEY ({column_name}_ref) "
                           f"REFERENCES {ref_table}({ref_column})")
            self.conn.commit()
            print(f"Clave foránea creada en '{table_name}' que referencia a '{ref_table}({ref_column})'.")
        except Error as e:
            print(f"Error al crear la clave foránea: {e}")


