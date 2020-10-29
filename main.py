import sqlite3
import csv
import re

import pandas as pd # to load column names and their data types

csv_file = "student-mat.csv"
df_from_csv = pd.read_csv(csv_file, delimiter=';')
table_name = input("Please enter the table name (string that doesn't start with '_sqlite'): ")

def get_proper_table_name(table_name):
    '''
    According to sqlite documentation (https://www.sqlite.org/lang_createtable.html),
    every string name for table is allowed, in spite of names starting with "slite_".
    '''
    if table_name == None or '':
        raise Exception("The table name cannot be None object or blank. Please change.")
    elif table_name == 'sqlite_':
        raise Exception("The table name cannot starts with 'sqlite_'. Please change.")
    elif isinstance(table_name[0], int):
        raise Exception("The table name cannot start with a digit. Please change.")
    elif not isinstance(table_name, str):
        table_name = str(table_name)

    return table_name


def create_table(df_dataset, table_name):
    '''
    The function returns SQL statement "CREATE TABLE" with needed table name
    and its column names along with data types which these columns will store.
    '''
    cols_with_sql_types = []
    for col_name, col_type in df_dataset.dtypes.iteritems():
        if col_type == "object":
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'TEXT')
        elif col_type == "int64":
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'INTEGER')

    final = str(cols_with_sql_types).replace("'", "").replace(']', '').replace('[', '')
    return f'CREATE TABLE "{table_name}" ({final})'

def drop_table_if_exists(table_name):
    '''
    The function returns SQL statement "DROP TABLE IF EXISTS" with needed table name.
    '''

    return f'DROP TABLE IF EXISTS {table_name}'

conn = sqlite3.connect('students.sqlite')
cur = conn.cursor()
cur.execute(f"{drop_table_if_exists(get_proper_table_name(table_name))}")
cur.execute(f"{create_table(df_from_csv, get_proper_table_name(table_name))}")

def insert_into_values(df_dataset, table_name):
    '''
    The function returns SQL statement "INSERT INTO" with needed table name and values.
    '''
    numb_of_columns = len(df_dataset.columns)
    values = str(['?' for i in range(numb_of_columns)]).replace("'", "").replace(']', '').replace('[', '')
    return f'INSERT INTO "{table_name}" VALUES ({values})'

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
