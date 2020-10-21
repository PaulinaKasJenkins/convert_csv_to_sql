import sqlite3
import csv
import re

import pandas as pd # to load column names and their data types

csv_file = "student-mat.csv"

df_from_csv = pd.read_csv(csv_file, delimiter=';')

def create_table(df_dataset, table_name):
    cols_with_sql_types = []
    for col_name, col_type in df_dataset.dtypes.iteritems():
        if col_type == "object":
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'TEXT')
        elif col_type == "int64":
            cols_with_sql_types.append('"' + col_name + '"' + " " + 'INTEGER')

    final = str(cols_with_sql_types).replace("'", "").replace(']', '').replace('[', '')
    return f'CREATE TABLE "{table_name}" ({final})'

def drop_table_if_exists(table_name):
    return f'DROP TABLE IF EXISTS {table_name}'

conn = sqlite3.connect('students.sqlite')
cur = conn.cursor()
cur.execute(f"{drop_table_if_exists('students')}")
cur.execute(f"{create_table(df_from_csv, 'students')}")

def insert_into_values(df_dataset, table_name):
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


        cur.execute(f"{insert_into_values(df_from_csv, 'students')}",
        tuple(lis))
        conn.commit()
