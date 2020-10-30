import pytest
import inspect
import pandas as pd
import numpy as np

from main import *

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
     - category
    '''

    # example dataset with dtypes that we want to test
    df_dataset = pd.DataFrame(
            data={'object': np.array(['foo'], dtype=object),
                  'int64': np.array([1], dtype=int),
                  'float64': np.array([0.5], dtype=float),
                  'bool': np.array([True], dtype=bool),
                  'datetime64': np.array([pd.Timestamp('20180310')], dtype=np.datetime64),
                  'timedelta[ns]': np.array([pd.Timedelta('1 days 06:05:01.000030')], dtype=np.timedelta64),
                  },
            index=[0],
            )

    # column for categorical dtype has been created here because
    # numpy do not recognize 'category' type
    df_dataset['category'] = 'B'
    df_dataset['category'].astype('category')

    def test_if_object_is_correctly_assigned_to_sqlite_dtypes(self):
        table_name = 'whatever'
        column_names = df_dataset.columns()
        final = '"object" TEXT, "int64" INTEGER, "float64" REAL, ...'

        assert create_table(df_dataset, table_name) == f'CREATE TABLE "{table_name}" ({final})'

    def test_if_int64_is_correctly_assigned_to_sqlite_dtypes(self):
        pass

    def test_if_float64_is_correctly_assigned_to_sqlite_dtypes(self):
        pass

    def test_if_datetime64_is_correctly_assigned_to_sqlite_dtypes(self):
        pass

    def test_if_timedeltans_is_correctly_assigned_to_sqlite_dtypes(self):
        pass

    def test_if_category_is_correctly_assigned_to_sqlite_dtypes(self):
        pass
