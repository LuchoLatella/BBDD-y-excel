import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
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

        # Botón para abrir una base de datos existente
        self.open_button = tk.Button(self.root, text="Open Existing DB", command=self.open_existing_database)
        self.open_button.grid(row=3, column=0, columnspan=2)

        # Botón para exportar datos
        self.export_button = tk.Button(self.root, text="Export Data", command=self.export_data)
        self.export_button.grid(row=4, column=0, columnspan=2)

        # Botón para ejecutar queries
        self.query_button = tk.Button(self.root, text="Execute Query", command=self.execute_query)
        self.query_button.grid(row=5, column=0, columnspan=2)

    def connect_to_database(self):
        """ Conecta a la base de datos MySQL. """
        db_name = self.db_entry.get()
        if not db_name:
            messagebox.showwarning("Error", "Please enter a database name.")
            return

        self.db_manager = DatabaseManager(db_name)
        self.db_manager.create_or_connect_db()
        self.conn = self.db_manager.connect()

    def open_existing_database(self):
        """ Permite al usuario seleccionar y abrir una base de datos existente. """
        self.db_manager = DatabaseManager()
        databases = self.db_manager.list_databases()
        if not databases:
            messagebox.showwarning("Error", "No databases found or failed to connect to the server.")
            return
        
        db_name = simpledialog.askstring("Select Database", "Enter the database name to connect:", initialvalue=databases[0])
        if db_name and db_name in databases:
            self.db_manager = DatabaseManager(db_name)
            self.conn = self.db_manager.connect()
            if self.conn:
                messagebox.showinfo("Success", f"Connected to database '{db_name}'.")
            else:
                messagebox.showerror("Error", f"Failed to connect to database '{db_name}'.")
        else:
            messagebox.showwarning("Error", "Database not found.")

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

    def execute_query(self):
        """ Permite al usuario ejecutar una consulta SQL en la base de datos. """
        if not self.conn:
            messagebox.showwarning("Error", "Please connect to a database first.")
            return
        
        query = simpledialog.askstring("Execute Query", "Enter SQL query:")
        if query:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Query Results:")
                for row in results:
                    print(row)
                self.conn.commit()
                messagebox.showinfo("Success", "Query executed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute query: {str(e)}")

# Inicia la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
