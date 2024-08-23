import pandas as pd
from tkinter import messagebox, filedialog

class QueryExecutor:
    def __init__(self, conn):
        self.conn = conn

    def export_to_csv(self, table_name, file_path):
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            df.to_csv(file_path, index=False)
            print(f"Data exported from table '{table_name}' to '{file_path}'.")
        except Exception as e:
            print(f"Failed to export data to CSV: {str(e)}")

    def export_to_excel(self, table_name, file_path):
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            df.to_excel(file_path, index=False, engine='openpyxl')
            print(f"Data exported from table '{table_name}' to '{file_path}'.")
        except Exception as e:
            print(f"Failed to export data to Excel: {str(e)}")

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.conn = None  # Conexión a la base de datos

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Elementos de la interfaz gráfica...
        # Botón para exportar datos
        self.export_button = tk.Button(self.root, text="Export Data", command=self.export_data)
        self.export_button.grid(row=3, column=0, columnspan=3)

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
