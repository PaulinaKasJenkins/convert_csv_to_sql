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

def fill_values_in(csv_file, df_from_csv, table_name):
    with open(csv_file) as csv_file_with_open:
        csv_reader = csv.reader(csv_file_with_open, delimiter=';')
        columns_number = [i for i in range(len(df_from_csv.columns))]
        variables = [f'variable{i}' for i in columns_number]

        next(csv_reader) # to skip header
        for row in csv_reader:
            dic = dict(zip(variables, row))

            tup = ()
            lis = list(tup)
            for i in variables:
                lis.append(dic[i])

            cur.execute(f"{insert_into_values(df_from_csv, table_name)}",
            tuple(lis))
            conn.commit()

    read_from_sql = pd.read_sql(f"select * from {table_name}", con = conn)
    return read_from_sql

print(fill_values_in(csv_file = csv_file,
                     df_from_csv = df_from_csv,
                     table_name = generated_table_name))
