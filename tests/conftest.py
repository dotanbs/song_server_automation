import pytest
from poject_logic import request_actions as do
from poject_logic import tests_logic
import json


@pytest.fixture(scope='function')
def json_config():
    do.delete_all_users()
    do.delete_all_songs()
    with open('tests/config.json') as fp:
        js_config = json.load(fp)
    for i in js_config['users']:
        do.add_user(i)
    for i in js_config['songs']:
        do.add_song(i)
    do.add_playlist(js_config['users'][2], js_config['playlists'][2])
    do.add_song_to_playlist(js_config['users'][2], js_config['playlists'][2], js_config['songs'][2])
    yield js_config








