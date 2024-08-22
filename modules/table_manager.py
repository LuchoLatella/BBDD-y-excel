import pandas as pd

import pandas as pd

def process_file(file):
    try:
        if file.filename.endswith('.csv'):
            return pd.read_csv(file, encoding='utf-8', delimiter=',', quotechar='"', error_bad_lines=False)
        else:
            return pd.read_excel(file)
    except UnicodeDecodeError:
        if file.filename.endswith('.csv'):
            return pd.read_csv(file, encoding='latin1', delimiter=',', quotechar='"', error_bad_lines=False)
        else:
            return pd.read_excel(file)


def create_new_table(df, selected_columns):
    return df[selected_columns]

def merge_dataframes(df1, df2, on_column):
    return pd.merge(df1, df2, on=on_column)
