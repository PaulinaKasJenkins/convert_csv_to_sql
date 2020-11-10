import sqlite3
import csv
import re

import pandas as pd # to load column names and their data types
import random, string # to generate random table name if necessary

csv_file = "students.csv"
df_from_csv = pd.read_csv(csv_file, delimiter=';')


def get_table_name(csv_file):
    '''
    Create a table name from CSV file name and convert it to be table name
    allowed by slite3 documentation.
    '''
    # when in CSV file name there are letters too
    regex = re.compile('[^a-z]')
    table_name = csv_file.split(".")[0]
    table_name = regex.sub('', table_name)

    # when in CSV file name there aren't any letters
    if table_name == '':
        for i in range(10):
            table_name += random.choice(string.ascii_lowercase)
    return table_name

generated_table_name = get_table_name(csv_file)

def create_table(df_dataset, table_name):
    '''
    The function returns SQL statement "CREATE TABLE" with needed table name
    and its column names along with data types which these columns will store.
    '''
    cols_with_sql_types = []
    for col_name, col_type in df_dataset.dtypes.iteritems():
        if col_type == "int64":
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'INTEGER')
        elif col_type == "float64":
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'REAL')
        else:
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'TEXT')

    final = str(cols_with_sql_types).replace("'", "").replace(']', '').replace('[', '')
    return f'CREATE TABLE "{table_name}" ({final})'

def drop_table_if_exists(table_name):
    '''
    The function returns SQL statement "DROP TABLE IF EXISTS" with needed table name.
    '''

    return f'DROP TABLE IF EXISTS {table_name}'


conn = sqlite3.connect(f'{generated_table_name}.sqlite')
cur = conn.cursor()
cur.execute(f"{drop_table_if_exists(generated_table_name)}")
cur.execute(f"{create_table(df_from_csv, generated_table_name)}")


def insert_into_values(df_dataset, table_name):
    '''
    The function returns SQL statement "INSERT INTO" with needed table name and values.
    '''
    numb_of_columns = len(df_dataset.columns)
    values = str(['?' for i in range(numb_of_columns)]).replace("'", "").replace(']', '').replace('[', '')
    return f'INSERT INTO "{table_name}" VALUES ({values})'


def convert_to_str(df_dataset):
    '''
    The function converts problematic dtypes to strings.
    '''
    for i in df_dataset.select_dtypes(include=['datetime', 'timedelta']):
        df_dataset[i] = df_dataset[i].astype(str)

    return df_dataset


def executemany(df_dataset, table_name):
    with sqlite3.connect(f'{table_name}.sqlite'):
        conn = sqlite3.connect(f'{table_name}.sqlite')
        cur = conn.cursor()

        for i in df_dataset.select_dtypes(include=['datetime', 'timedelta']):
            df_dataset[i] = df_dataset[i].astype(str)

        values = convert_to_str(df_dataset).values.tolist()

        cur.executemany(f"{insert_into_values(df_dataset, table_name)}", values)
        conn.commit()

executemany(df_from_csv, generated_table_name)
