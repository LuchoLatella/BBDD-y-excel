from flask import Flask, request, render_template, redirect, url_for
from modules import file_handler, database, filter, updater

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        df = file_handler.process_file(file)
        database.save_dataframe_to_db(df, 'temp_table')
        return redirect(url_for('select_columns'))
    return "No se ha subido ningún archivo"

@app.route('/select_columns', methods=['GET', 'POST'])
def select_columns():
    df = database.load_dataframe_from_db('temp_table')
    if request.method == 'POST':
        selected_columns = request.form.getlist('columns')
        new_df = file_handler.create_new_table(df, selected_columns)
        database.save_dataframe_to_db(new_df, 'new_table')
        return "Nueva tabla creada con columnas seleccionadas"
    return render_template('select_columns.html', columns=df.columns)

@app.route('/filter', methods=['GET', 'POST'])
def filter_data():
    df = database.load_dataframe_from_db('temp_table')
    if request.method == 'POST':
        filter_column = request.form['filter_column']
        filter_value = request.form['filter_value']
        filtered_df = filter.apply_filter(df, filter_column, filter_value)
        database.save_dataframe_to_db(filtered_df, 'filtered_table')
        return "Datos filtrados y guardados en nueva tabla"
    return render_template('filter.html', columns=df.columns)

@app.route('/update_mass', methods=['GET', 'POST'])
def update_mass():
    if request.method == 'POST':
        update_column = request.form['update_column']
        new_value = request.form['new_value']
        updater.update_mass('temp_table', update_column, new_value)
        return "Datos actualizados en masa"
    return render_template('update_mass.html', columns=database.get_columns('temp_table'))

@app.route('/merge', methods=['POST'])
def merge_files():
    file = request.files['file']
    if file:
        new_df = file_handler.process_file(file)
        df = database.load_dataframe_from_db('temp_table')
        merged_df = file_handler.merge_dataframes(df, new_df, 'common_column')  # Define 'common_column'
        database.save_dataframe_to_db(merged_df, 'merged_table')
        return "Archivos combinados y guardados en una nueva tabla"
    return "No se ha subido ningún archivo"

if __name__ == '__main__':
    app.run(debug=True)
