from pojetc_logic import request_actions, tests_logic


def test_add_user():
    res = request_actions.add_user('dotan', '123456')
    res = request_actions.get_user('dotan')
    assert tests_logic.validate_key_value(res, 'user_name', 'dotan'), 'user_name was not found'


def test_add_song():
    res = request_actions.add_song('rock', '1989', 'bruce', 'love_to_rock2')
    assert not tests_logic.found_error(res), 'could not add song'
    res = request_actions.get_song('love_to_rock2')
    assert tests_logic.validate_key_value(res, 'title', 'love_to_rock2')


def test_add_playlist(json_config):
    user = json_config['users'][1]
    request_actions.add_playlist(user['user_name'], user['user_password'], 'playlist2')
    res = request_actions.get_playlist(user['user_name'], user['user_password'], 'playlist2')
    assert not tests_logic.found_error(res), 'could not add playlist'


def test_add_song_to_playlist(json_config):
    user = json_config['users'][0]
    song = json_config['songs'][0]
    # res = request_actions.add_song('rock', '1989', 'bruce', 'love_to_rock4')
    # assert not tests_logic.found_error(res), 'could not add song'
    res = request_actions.add_playlist(user['user_name'], user['user_password'], 'playlist1')
    # res = request_actions.get_playlist(user['user_name'], user['user_password'], 'playlist1')
    res = request_actions.add_song_to_playlist(user['user_name'], user['user_password'], 'playlist1',
                                               song['song_title'])
    assert not tests_logic.found_error(res), 'could not add song to playlist'
    res = request_actions.get_playlist(user['user_name'], user['user_password'], 'playlist1')
    assert tests_logic.validate_key_value(res, 'title', song['song_title'])


def test_add_friend():
    request_actions.add_user('dotan2', '123456')
    request_actions.add_user('dotan3', '123456')
    request_actions.add_friend('dotan', '123456', 'dotan3')
    res = request_actions.get_user('dotan')
    assert tests_logic.validate_key_value(res, 'user_name', 'dotan'), 'user_name was not found'

# def test_add_user():
#     request_actions.add_user('dotan', '123456')
#     assert request_actions.get_user('ppp')
