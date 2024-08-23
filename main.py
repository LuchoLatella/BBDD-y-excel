import tkinter as tk
from tkinter import filedialog, messagebox
from modules.db_manager import DatabaseManager
from modules.table_manager import TableManager
from modules.data_import import DataImport
from modules.query_executor import QueryExecutor

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.db_manager = None
        self.conn = None

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Create Database
        self.db_label = tk.Label(self.root, text="Database Name:")
        self.db_label.grid(row=0, column=0)
        self.db_entry = tk.Entry(self.root)
        self.db_entry.grid(row=0, column=1)
        self.db_button = tk.Button(self.root, text="Create/Connect", command=self.create_or_connect_db)
        self.db_button.grid(row=0, column=2)

        # Create Table
        self.table_label = tk.Label(self.root, text="Table Name:")
        self.table_label.grid(row=1, column=0)
        self.table_entry = tk.Entry(self.root)
        self.table_entry.grid(row=1, column=1)
        self.table_button = tk.Button(self.root, text="Create Table", command=self.create_table)
        self.table_button.grid(row=1, column=2)

        # Import CSV
        self.import_button = tk.Button(self.root, text="Import CSV", command=self.import_csv)
        self.import_button.grid(row=2, column=0, columnspan=3)

    def create_or_connect_db(self):
        db_name = self.db_entry.get()
        if db_name:
            self.db_manager = DatabaseManager(db_name)
            self.db_manager.create_database()
            self.conn = self.db_manager.connect()
            messagebox.showinfo("Success", f"Connected to database {db_name}")
        else:
            messagebox.showwarning("Error", "Please enter a database name.")

    def create_table(self):
        if not self.conn:
            messagebox.showwarning("Error", "Please connect to a database first.")
            return
        table_name = self.table_entry.get()
        if table_name:
            columns = {
                'id': 'INTEGER PRIMARY KEY',
                'name': 'TEXT',
                'age': 'INTEGER',
                'email': 'TEXT'
            }
            table_manager = TableManager(self.conn)
            table_manager.create_table(table_name, columns)
            messagebox.showinfo("Success", f"Table {table_name} created.")
        else:
            messagebox.showwarning("Error", "Please enter a table name.")

    def import_csv(self):
        if not self.conn:
            messagebox.showwarning("Error", "Please connect to a database first.")
            return
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            data_import = DataImport(self.conn)
            table_name = self.table_entry.get() or "imported_table"
            data_import.import_from_csv(file_path, table_name)
            messagebox.showinfo("Success", f"Data imported into table {table_name}.")
        else:
            messagebox.showwarning("Error", "No file selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

