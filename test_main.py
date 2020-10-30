import pytest
import inspect

from main import *

class Test_create_table():
    def test_


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
