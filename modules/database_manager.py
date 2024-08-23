import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, db_name=None, user='root', password='', host='localhost'):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.conn = None

    def create_or_connect_db(self):
        """ Conecta a la base de datos MySQL o la crea si no existe. """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = self.conn.cursor()
            if self.db_name:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
                cursor.execute(f"USE {self.db_name}")
                self.conn.commit()
            print(f"Base de datos '{self.db_name}' conectada o creada exitosamente.")
        except Error as e:
            print(f"Error al conectar o crear la base de datos: {e}")

    def connect(self):
        """ Establece la conexión a la base de datos. """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            return self.conn
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def list_databases(self):
        """ Lista todas las bases de datos disponibles en el servidor. """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = self.conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            return databases
        except Error as e:
            print(f"Error al listar las bases de datos: {e}")
            return []

    def close_connection(self):
        """ Cierra la conexión a la base de datos. """
        if self.conn:
            self.conn.close()
            print("Conexión cerrada.")
