import pandas as pd

def process_file(file):
    if file.filename.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def create_new_table(df, selected_columns):
    return df[selected_columns]

def merge_dataframes(df1, df2, on_column):
    return pd.merge(df1, df2, on=on_column)
