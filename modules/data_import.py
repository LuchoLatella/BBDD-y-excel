import pandas as pd

class DataImport:
    def __init__(self, conn):
        self.conn = conn

    def import_from_csv(self, file_path, table_name):
        df = pd.read_csv(file_path)
        df.to_sql(table_name, self.conn, if_exists='append', index=False)
        print(f"Datos importados desde '{file_path}' a la tabla '{table_name}'.")

    def import_from_excel(self, file_path, table_name):
        df = pd.read_excel(file_path)
        df.to_sql(table_name, self.conn, if_exists='append', index=False)
        print(f"Datos importados desde '{file_path}' a la tabla '{table_name}'.")
