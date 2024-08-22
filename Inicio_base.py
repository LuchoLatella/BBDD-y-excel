from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import sqlite3

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para cargar y procesar los archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        df = pd.read_csv(file) if file.filename.endswith('.csv') else pd.read_excel(file)
        
        # Guardar las columnas en la base de datos temporal
        conn = sqlite3.connect('mi_base_de_datos.db')
        df.to_sql('temp_table', conn, if_exists='replace', index=False)
        conn.close()

        # Redirigir a la página para elegir columnas
        return redirect(url_for('select_columns'))

    return "No se ha subido ningún archivo"

# Ruta para seleccionar columnas y crear nuevas tablas
@app.route('/select_columns', methods=['GET', 'POST'])
def select_columns():
    conn = sqlite3.connect('mi_base_de_datos.db')
    df = pd.read_sql_query("SELECT * FROM temp_table", conn)
    conn.close()

    if request.method == 'POST':
        selected_columns = request.form.getlist('columns')
        new_df = df[selected_columns]
        
        conn = sqlite3.connect('mi_base_de_datos.db')
        new_df.to_sql('new_table', conn, if_exists='replace', index=False)
        conn.close()
        
        return "Nueva tabla creada con columnas seleccionadas"

    return render_template('select_columns.html', columns=df.columns)

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
