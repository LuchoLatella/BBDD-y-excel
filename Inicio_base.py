import pandas as pd
import sqlite3


# Cargar desde un archivo CSV
df_csv = pd.read_csv('archivo.csv')

# Cargar desde un archivo Excel
df_excel = pd.read_excel('archivo.xlsx', sheet_name='Sheet1')


conn = sqlite3.connect('mi_base_de_datos.db')
cursor = conn.cursor()


# Crear una tabla con las columnas del DataFrame
df_csv.to_sql('tabla_csv', conn, if_exists='replace', index=False)
df_excel.to_sql('tabla_excel', conn, if_exists='replace', index=False)
