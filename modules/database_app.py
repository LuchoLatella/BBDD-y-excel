import tkinter as tk
from tkinter import messagebox, filedialog
from query_executor import QueryExecutor  # Asegúrate de importar QueryExecutor correctamente

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.conn = None  # Conexión a la base de datos

        # Crear elementos de la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        """ Crea y organiza los elementos de la interfaz gráfica. """
        tk.Label(self.root, text="Table Name:").grid(row=0, column=0)
        self.table_entry = tk.Entry(self.root)
        self.table_entry.grid(row=0, column=1)

        # Botón para exportar datos
        self.export_button = tk.Button(self.root, text="Export Data", command=self.export_data)
        self.export_button.grid(row=1, column=0, columnspan=2)

    def export_data(self):
        """ Maneja la exportación de datos a CSV o Excel desde la interfaz gráfica. """
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
