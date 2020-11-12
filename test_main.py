import pytest
import inspect
import pandas as pd
import numpy as np
import os.path

from main import *

@pytest.fixture(scope="module")
def dataframe_to_test():
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

    return df_dataset

class Test_get_table_name:

    # when in CSV file name there are letters too
    @pytest.mark.parametrize("csv_file", ["123abc.csv", "---abc.csv"])
    def test_if_name_starts_with_not_allowed_chars_then_letters(self, csv_file):
        generated_table_name = get_table_name(csv_file)

        expected = 3
        assert len(generated_table_name) == expected

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

        expected = 10
        assert len(generated_table_name) == expected

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

    def test_if_pandas_dtypes_are_correctly_assigned_to_sqlite_dtypes(self, dataframe_to_test):
        table_name = 'abc'
        expected = '"object" TEXT, "int64" INTEGER, "float64" REAL, "bool" TEXT, "datetime64ns" TEXT, "timedelta64ns" TEXT'

        assert create_table(dataframe_to_test, table_name) == f'CREATE TABLE "{table_name}" ({expected})'

class Test_drop_table_if_exists:

    def test_if_returned_value_is_correct(self):
        csv_file = "abc.csv"
        generated_table_name = get_table_name(csv_file) # func get_table_name(csv_file) has been already tested

        expected = f'DROP TABLE IF EXISTS abc'
        assert drop_table_if_exists(generated_table_name) == expected


class Test_insert_into_values:

    def test_if_returned_value_is_correct(self, dataframe_to_test):
        csv_file = "abc.csv"
        generated_table_name = get_table_name(csv_file) # func get_table_name(csv_file) has been already tested

        expected = f'INSERT INTO "abc" VALUES (?, ?, ?, ?, ?, ?)'
        assert insert_into_values(dataframe_to_test, generated_table_name) == expected


class Test_executemany:

    def test_if_db_is_correctly_saved(self, dataframe_to_test):
        csv_file = "abc.csv"
        dataframe_to_test.to_csv(csv_file, index=False, sep=';')
        generated_table_name = get_table_name(csv_file) # func get_table_name(csv_file) has been already tested

        conn = sqlite3.connect(f'{generated_table_name}.sqlite')
        cur = conn.cursor()

        cur.execute(f"{drop_table_if_exists(generated_table_name)}")
        cur.execute(f"{create_table(dataframe_to_test, generated_table_name)}")

        executemany(dataframe_to_test, generated_table_name)

        expected = 1
        assert len(cur.execute(f'select * from {generated_table_name}').fetchall()) == expected


class Test_convert_to_str:

    def test_if_dataframe_is_ok(self, dataframe_to_test):
        expected = pd.DataFrame(
                data={'object': np.array(['foo'], dtype=object),
                      'int64': np.array([1], dtype=int),
                      'float64': np.array([0.5], dtype=float),
                      'bool': np.array([True], dtype=bool),
                      'datetime64ns': '2018-03-10',
                      'timedelta64ns': '1 days 06:05:01.000030',
                      },
                index=[0],
                )
        pd.testing.assert_frame_equal(expected, convert_to_str(dataframe_to_test))
