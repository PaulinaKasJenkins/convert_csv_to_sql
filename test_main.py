import pytest
import inspect

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
