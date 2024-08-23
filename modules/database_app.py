import tkinter as tk
from tkinter import messagebox, filedialog
from database_manager import DatabaseManager
from query_executor import QueryExecutor
from table_manager import TableManager

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.conn = None

        # Crear elementos de la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        """ Crea y organiza los elementos de la interfaz gráfica. """
        tk.Label(self.root, text="Database Name:").grid(row=0, column=0)
        self.db_entry = tk.Entry(self.root)
        self.db_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Table Name:").grid(row=1, column=0)
        self.table_entry = tk.Entry(self.root)
        self.table_entry.grid(row=1, column=1)

        # Botón para conectar a la base de datos
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_database)
        self.connect_button.grid(row=2, column=0, columnspan=2)

        # Botón para exportar datos
        self.export_button = tk.Button(self.root, text="Export Data", command=self.export_data)
        self.export_button.grid(row=3, column=0, columnspan=2)

    def connect_to_database(self):
        """ Conecta a la base de datos MySQL. """
        db_name = self.db_entry.get()
        if not db_name:
            messagebox.showwarning("Error", "Please enter a database name.")
            return

        self.db_manager = DatabaseManager(db_name)
        self.db_manager.create_or_connect_db()
        self.conn = self.db_manager.connect()

    def export_data(self):
        """ Exporta datos a CSV o Excel. """
        if not self.conn:
            messagebox.showwarning("Error", "Please connect to a database first.")
            return
        
        table_name = self.table_entry.get()
        if not table_name:
            messagebox.showwarning("Error", "Please enter a table name.")
            return

        file_path = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            query_executor = QueryExecutor(self.conn)
            if file_path.endswith('.csv'):
                query_executor.export_to_csv(table_name, file_path)
            elif file_path.endswith('.xlsx'):
                query_executor.export_to_excel(table_name, file_path)
            else:
                messagebox.showwarning("Error", "Unsupported file format.")
                return
            messagebox.showinfo("Success", f"Data exported to {file_path}.")

# Inicia la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
