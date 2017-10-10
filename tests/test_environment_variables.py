import os

from lambda_local.environment_variables import set_environment_variables


def test_set_environment_variables():
    os.getenv('STR_KEY') is None
    os.getenv('INT_KEY') is None
    os.getenv('BOOL_KEY') is None

    set_environment_variables('tests/environment_variables.json')

    assert os.getenv('STR_KEY') == 'foo'
    assert os.getenv('INT_KEY') == '100'
    assert os.getenv('BOOL_KEY') == 'False'
