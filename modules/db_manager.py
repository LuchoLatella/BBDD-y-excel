import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(os.path.join('databases', self.db_name))
        return self.conn

    def create_database(self):
        if not os.path.exists('databases'):
            os.makedirs('databases')
        self.connect()
        print(f"Base de datos '{self.db_name}' creada y conectada.")

    def list_databases(self):
        return [f for f in os.listdir('databases') if f.endswith('.db')]

    def close_connection(self):
        if self.conn:
            self.conn.close()

