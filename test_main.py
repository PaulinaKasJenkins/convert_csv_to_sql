import pytest
import inspect

from main import *

class Test_get_table_name:

    @pytest.mark.parametrize("csv_file", ["sqlite_.csv", "sqlite_aabbcc.csv"])
    def test_if_name_starts_with_sqlite__is_not_allowed(self, csv_file):
        '''
        As we don't know what exactly get_table_name() will return because of
        random module, we will check characteristics like len() and letters.
        '''
        assert len(get_table_name()) == 10 # length should be equal to 10

        regex = re.compile('[^a-z]') # letters inside should be ascii lowercase
        assert get_table_name() == regex.sub('', get_table_name())



# class Test_drop_table_if_exists:
#     def test_input_var_types_int(self):
#         input = 123
#         assert drop_table_if_exists(input) == 'DROP TABLE IF EXISTS 123'
#
#     def test_input_var_types_str(self):
#         input = 'table'
#         assert drop_table_if_exists(input) == 'DROP TABLE IF EXISTS table'
#
#     def test_input_var_types_none(self):
#         input = None
#         with pytest.raises(Exception) as excinfo:
#             drop_table_if_exists(input)
#         assert str(excinfo.value) == 'The table name cannot be None object. Please change.'
#
#     def test_input_var_types_sqlite(self):
#         input = 'sqlite_'
#         with pytest.raises(Exception) as excinfo:
#             drop_table_if_exists(input)
#         assert str(excinfo.value) == "The table name cannot starts with 'sqlite_'. Please change."
