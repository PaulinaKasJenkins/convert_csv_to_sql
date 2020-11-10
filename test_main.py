import pytest
import inspect
import pandas as pd
import numpy as np
import os.path

from main import *

'''
Functional Database Testing
https://www.guru99.com/data-testing.html
https://speakerdeck.com/wpuclark/database-testing-with-pytest?slide=17
'''

class Test_get_table_name:

    # when in CSV file name there are letters too
    @pytest.mark.parametrize("csv_file", ["123abc.csv", "---abc.csv"])
    def test_if_name_starts_with_not_allowed_chars_then_letters(self, csv_file):
        generated_table_name = get_table_name(csv_file)

        expected_length = 3
        assert len(generated_table_name) == expected_length

        regex = re.compile('[^a-z]') # letters inside should be ascii lowercase
        assert generated_table_name == regex.sub('', generated_table_name)

    # when in CSV file name there aren't any letters
    @pytest.mark.parametrize("csv_file", ["123.csv", "---.csv"])
    def test_if_name_with_only_not_allowed_chars(self, csv_file):
        '''
        As we don't know what exactly get_table_name() will return because of
        random module, we will check characteristics like len() and letters.
        '''
        generated_table_name = get_table_name(csv_file)

        expected_length = 10
        assert len(generated_table_name) == expected_length

        regex = re.compile('[^a-z]') # letters inside should be ascii lowercase
        assert generated_table_name == regex.sub('', generated_table_name)

class Test_create_table:
    '''
    Pandas possible dtypes:                 Sqlite3 possible dtypes:
     - object                               - null
     - int64                                - integer
     - float64                              - real
     - bool                                 - text
     - datetime64                           - blob
     - timedelta[ns]
    '''

    def test_if_pandas_dtypes_are_correctly_assigned_to_sqlite_dtypes(self):

        # example dataset with dtypes that we want to test
        df_dataset = pd.DataFrame(
                data={'object': np.array(['foo'], dtype=object),
                      'int64': np.array([1], dtype=int),
                      'float64': np.array([0.5], dtype=float),
                      'bool': np.array([True], dtype=bool),
                      'datetime64ns': np.array([pd.Timestamp('20180310')], dtype=np.datetime64),
                      'timedelta64ns': np.array([pd.Timedelta('1 days 06:05:01.000030')], dtype=np.timedelta64),
                      },
                index=[0],
                )
        table_name = 'whatever'
        expected_final = '"object" TEXT, "int64" INTEGER, "float64" REAL, "bool" TEXT, "datetime64ns" TEXT, "timedelta64ns" TEXT'

        assert create_table(df_dataset, table_name) == f'CREATE TABLE "{table_name}" ({expected_final})'

class Test_drop_table_if_exists:

    def test_if_returned_value_is_correct(self):
        csv_file = "abc.csv"
        generated_table_name = get_table_name(csv_file) # func get_table_name(csv_file) has been already tested
        assert drop_table_if_exists(generated_table_name) == f'DROP TABLE IF EXISTS {generated_table_name}'

class Test_insert_into_values:

    def test_if_returned_value_is_correct(self):
        csv_file = "abc.csv"
        generated_table_name = get_table_name(csv_file) # func get_table_name(csv_file) has been already tested
        df_dataset = pd.DataFrame(
                data={'object': np.array(['foo'], dtype=object),
                      'int64': np.array([1], dtype=int),
                      'float64': np.array([0.5], dtype=float),
                      'bool': np.array([True], dtype=bool),
                      'datetime64ns': np.array([pd.Timestamp('20180310')], dtype=np.datetime64),
                      'timedelta64ns': np.array([pd.Timedelta('1 days 06:05:01.000030')], dtype=np.timedelta64),
                      },
                index=[0],
                )
        numb_of_columns = len(df_dataset.columns)
        values = str(['?' for i in range(numb_of_columns)]).replace("'", "").replace(']', '').replace('[', '')
        assert insert_into_values(df_dataset, generated_table_name) == f'INSERT INTO "{generated_table_name}" VALUES ({values})'

class Test_executemany:

<<<<<<< HEAD
class Test_fill_values_in:

    @pytest.mark.parametrize('generated_table_name', [get_table_name(csv_file)])
    def test_if_db_is_correctly_saved(self, generated_table_name):
        df_from_csv = pd.DataFrame(
=======
    def test_if_db_is_correctly_saved(self):
        df_from_csv_test = pd.DataFrame(
>>>>>>> spike_executemany
                data={'object': np.array(['foo'], dtype=object),
                      'int64': np.array([1], dtype=int),
                      'float64': np.array([0.5], dtype=float),
                      'bool': np.array([True], dtype=bool),
                      'datetime64ns': np.array([pd.Timestamp('20180310')], dtype=np.datetime64),
                      'timedelta64ns': np.array([pd.Timedelta('1 days 06:05:01.000030')], dtype=np.timedelta64),
                      },
                index=[0],
                )
        df_from_csv.to_csv("abc.csv", index=False, sep=';')
        csv_file = "abc.csv"
        columns_number = len(df_from_csv.columns)
        values = str(['?' for i in range(columns_number)]).replace("'", "").replace(']', '').replace('[', '')

        conn = sqlite3.connect(f'{generated_table_name}.sqlite')
        cur = conn.cursor()

        a = list(fill_values_in().columns)

        df_from_csv_test.to_csv("abc.csv", index=False, sep=';')
        csv_file_test = "abc.csv"
        generated_table_name_test = get_table_name(csv_file_test) # func get_table_name(csv_file) has been already tested

        conn = sqlite3.connect(f'{generated_table_name_test}.sqlite')
        cur = conn.cursor()
        cur.execute(f"{drop_table_if_exists(generated_table_name_test)}")
        cur.execute(f"{create_table(df_from_csv_test, generated_table_name_test)}")

        executemany(df_dataset=df_from_csv_test,
                    table_name=generated_table_name_test)

        assert len(cur.execute(f'select * from {table_name}').fetchall()) == 1
