import pytest
from pojetc_logic import request_actions as do
import json


# @pytest.fixture(scope='function')
# def create_users(json_config):
#     users = json_config['users']
#     do.set_users_into_db(users)
#
#
# @pytest.fixture(scope='function')
# def create_songs(json_config):
#     songs = json_config['songs']
#     do.set_users_into_db(songs)
#     return json_config


@pytest.fixture(scope='session')
def json_config(request):
    # file = pathlib.Path(request.node.fspath.strpath)
    # config = file.with_name('config.json')
    with open('tests/config.json') as fp:
        js_config = json.load(fp)
    for i in js_config['users']:
        do.add_user(i['user_name'], i['user_password'])
    for i in js_config['songs']:
        do.add_song(i['song_genre'], i['song_year'], i['song_performer'], i['song_title'])
    yield js_config
    do.delete_all_users()
    do.delete_all_songs()




