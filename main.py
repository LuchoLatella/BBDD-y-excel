from modules.db_manager import DatabaseManager
from modules.table_manager import TableManager
from modules.data_import import DataImport
from modules.query_executor import QueryExecutor

def main():
    # Crear y conectar a la base de datos
    db_name = input("Nombre de la base de datos (ej. 'mi_base_de_datos.db'): ")
    db_manager = DatabaseManager(db_name)
    db_manager.create_database()
    conn = db_manager.connect()

    # Crear una tabla
    table_name = input("Nombre de la tabla a crear: ")
    columns = {
        'id': 'INTEGER PRIMARY KEY',
        'name': 'TEXT',
        'age': 'INTEGER',
        'email': 'TEXT'
    }
    table_manager = TableManager(conn)
    table_manager.create_table(table_name, columns)

    # Importar datos desde un archivo CSV
    csv_path = input("Ruta del archivo CSV a importar: ")
    data_import = DataImport(conn)
    data_import.import_from_csv(csv_path, table_name)

    # Ejecutar una consulta
    query_executor = QueryExecutor(conn)
    query = f"SELECT * FROM {table_name}"
    results = query_executor.execute_query(query)
    for row in results:
        print(row)

    # Insertar datos manualmente
    data = {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}
    query_executor.insert_data(table_name, data)

    # Cerrar la conexión
    db_manager.close_connection()

if __name__ == "__main__":
    main()

