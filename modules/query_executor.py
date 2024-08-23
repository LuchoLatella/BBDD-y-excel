import pandas as pd
from mysql.connector import Error

class QueryExecutor:
    def __init__(self, conn):
        self.conn = conn

    def export_to_csv(self, table_name, file_path):
        """ Exporta los datos de la tabla a un archivo CSV. """
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            df.to_csv(file_path, index=False)
            print(f"Data exported from table '{table_name}' to '{file_path}'.")
        except Exception as e:
            print(f"Failed to export data to CSV: {str(e)}")

    def export_to_excel(self, table_name, file_path):
        """ Exporta los datos de la tabla a un archivo Excel. """
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            df.to_excel(file_path, index=False, engine='openpyxl')
            print(f"Data exported from table '{table_name}' to '{file_path}'.")
        except Exception as e:
            print(f"Failed to export data to Excel: {str(e)}")


    def export_data(self):
        if not self.conn:
            messagebox.showwarning("Error", "Please connect to a database first.")
            return
        
        table_name = self.table_entry.get()  # Obtener el nombre de la tabla desde la interfaz
        if not table_name:
            messagebox.showwarning("Error", "Please enter a table name.")
            return

        file_path = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            try:
                query_executor = QueryExecutor(self.conn)
                if file_path.endswith('.csv'):
                    query_executor.export_to_csv(table_name, file_path)
                elif file_path.endswith('.xlsx'):
                    query_executor.export_to_excel(table_name, file_path)
                else:
                    messagebox.showwarning("Error", "Unsupported file format.")
                    return
                messagebox.showinfo("Success", f"Data exported to {file_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
