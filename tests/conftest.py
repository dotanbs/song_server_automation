import pytest
from poject_logic import request_actions as do
from poject_logic import tests_logic
import json


@pytest.fixture(autouse=True, scope='function')
def json_config():
    do.delete_all_users()
    do.delete_all_songs()








