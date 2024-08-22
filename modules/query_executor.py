import sqlite3
from modules.database import connect_db

def update_mass(table_name, update_column, new_value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET {update_column} = ? WHERE {update_column} IS NOT NULL", (new_value,))
    conn.commit()
    conn.close()
