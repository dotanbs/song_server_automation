from poject_logic import request_actions, tests_logic
import pytest


# add user -> get user and validate it is exist
def test_add_user(json_config):
    user = tests_logic.build_user_dictionary('dotan', '123456')
    res = request_actions.add_user(user)
    assert not tests_logic.found_error(res), 'Failed to add user: ' + user['user_name']

    res = request_actions.get_user(user)
    assert tests_logic.validate_user_exist(res, user['user_name']), user['user_name'] + ' not found'


# add user -> get user and validate it is exist
def test_add_user_that_already_exist(json_config):
    user = json_config['users'][1]
    #user = tests_logic.build_user_dictionary('dotan', '123456')
    res = request_actions.add_user(user)
    assert tests_logic.found_error(res), 'expected to have error'


@pytest.mark.parametrize('rank, op, expected',
                         [('0', 'greater', ['song1', 'song2', 'song3']), ('2', 'less', ['song3', 'song4']),
                          ('3', 'eq', ['song1', 'song2'])])
def test_get_song_by_rank(json_config, rank, op, expected):
    tests_logic.create_songs_ranked(json_config)
    # song1 rank = 3, song2 rank = 3, song3 rank = 1
    res = request_actions.get_song_by_rank(rank, op)
    assert res['data'] == expected


# run add song and validate there are no errors and that the song exist
def test_add_song(json_config):
    song = tests_logic.build_song_dictionary('rock', '1989', 'bruce', 'love_to_rock2')
    res = request_actions.add_song(song)
    assert not tests_logic.found_error(res), 'Failed to add song'

    res = request_actions.get_song(song['song_title'])
    assert tests_logic.validate_song_exist(res, song['song_title'])


# add a playlist to a preconfigured user from tearup and make sure it was added
def test_add_playlist(json_config):
    user = json_config['users'][1]
    playlist = tests_logic.build_playlist_dictionary('playlist2')
    request_actions.add_playlist(user, playlist)
    res = request_actions.get_playlist(user, 'playlist2')
    assert not tests_logic.found_error(res), 'could not add playlist'


# add a playlist to a preconfigured user from tearup and make sure it was added
def test_add_multiple_playlist(json_config):
    user = json_config['users'][1]
    playlist1 = tests_logic.build_playlist_dictionary('pl_l1')
    playlist2 = tests_logic.build_playlist_dictionary('pl_l2')
    playlist3 = tests_logic.build_playlist_dictionary('pl_l3')

    request_actions.add_playlist(user, playlist1)
    request_actions.add_playlist(user, playlist2)
    request_actions.add_playlist(user, playlist3)

    res = request_actions.get_playlist(user, playlist1['playlist_name'])
    assert not tests_logic.found_error(res), 'could not get playlist: ' + playlist1['playlist_name']
    res = request_actions.get_playlist(user, playlist2['playlist_name'])
    assert not tests_logic.found_error(res), 'could not get playlist: ' + playlist2['playlist_name']
    res = request_actions.get_playlist(user, playlist3['playlist_name'])
    assert not tests_logic.found_error(res), 'could not get playlist: ' + playlist3['playlist_name']


# add same playlist name to 2 different users
def test_add_multiple_users_same_playlist_name(json_config):
    userA = json_config['users'][0]
    userB = json_config['users'][1]
    playlist1 = tests_logic.build_playlist_dictionary('pl_l1')

    request_actions.add_playlist(userA, playlist1)
    request_actions.add_playlist(userB, playlist1)

    res = request_actions.get_playlist(userA, playlist1['playlist_name'])
    assert not tests_logic.found_error(res), 'could not get playlist: ' + playlist1['playlist_name']
    res = request_actions.get_playlist(userB, playlist1['playlist_name'])
    assert not tests_logic.found_error(res), 'could not get playlist: ' + playlist1['playlist_name']


# add a playlist and a song and validate it is now in the song
def test_add_song_to_playlist(json_config):
    user = json_config['users'][0]
    song = json_config['songs'][0]
    playlist = tests_logic.build_playlist_dictionary('playlist1')

    res = request_actions.add_playlist(user, playlist)
    assert not tests_logic.found_error(res), 'could not add playlist'

    res = request_actions.add_song_to_playlist(user, playlist,
                                               song)
    assert not tests_logic.found_error(res), 'could not add song to playlist'

    res = request_actions.get_playlist(user, 'playlist1')
    assert tests_logic.validate_song_exist(res, song['song_title'])


# add a playlist and a multiple songs song and validate it is now in the playlist
def test_add_multiple_songs_to_playlist(json_config):
    user = json_config['users'][0]
    songA = json_config['songs'][0]
    songB = json_config['songs'][1]

    playlist = tests_logic.build_playlist_dictionary('playlist1')

    res = request_actions.add_playlist(user, playlist)

    request_actions.add_song_to_playlist(user, playlist,
                                         songA)
    request_actions.add_song_to_playlist(user, playlist,
                                         songB)

    res = request_actions.get_playlist(user, 'playlist1')
    assert tests_logic.validate_song_exist(res, songA['song_title'])
    assert tests_logic.validate_song_exist(res, songB['song_title'])


# take 2 users from config and add userB to userA
def test_add_friend(json_config):
    userA = json_config['users'][0]
    userB = json_config['users'][1]

    request_actions.add_friend(userA, userB)
    res = request_actions.get_user(userA)
    assert tests_logic.validate_friend_exist(res, userA, userB), 'user_name was not found'

    res = request_actions.get_user(userB)
    assert tests_logic.validate_friend_exist(res, userB, userA), 'user_name was not found'


def test_upvote_song(json_config):
    user = json_config['users'][2]
    song = json_config['songs'][2]
    pl = json_config['playlists'][2]

    res = request_actions.get_playlist(user, pl['playlist_name'])
    rank_before_upvote = tests_logic.get_rank(res, song)
    request_actions.song_upvote(user, pl, song)
    res = request_actions.get_playlist(user, pl['playlist_name'])
    rank_after_upvote = tests_logic.get_rank(res, song)
    assert rank_after_upvote is (rank_before_upvote + 1)


def test_downvote_song(json_config):
    user = json_config['users'][2]
    song = json_config['songs'][2]
    pl = json_config['playlists'][2]

    res = request_actions.get_playlist(user, pl['playlist_name'])
    rank_before_upvote = tests_logic.get_rank(res, song)
    request_actions.song_upvote(user, pl, song)
    res = request_actions.get_playlist(user, pl['playlist_name'])
    rank_after_upvote = tests_logic.get_rank(res, song)
    assert rank_after_upvote is (rank_before_upvote + 1)
    request_actions.song_downvote(user, pl, song)
    res = request_actions.get_playlist(user, pl['playlist_name'])
    rank_after_downvote = tests_logic.get_rank(res, song)
    assert rank_before_upvote is rank_after_downvote


def test_change_password(json_config):
    user = json_config['users'][2]
    pl = json_config['playlists'][2]
    new_password = '555555'
    request_actions.change_password(user, new_password)
    res = request_actions.get_playlist(user, pl['playlist_name'])
    assert tests_logic.found_error(res), 'found no error, but expected'
    user = tests_logic.build_user_dictionary(user['user_name'], new_password)
    res = request_actions.get_playlist(user, pl['playlist_name'])
    assert not tests_logic.found_error(res), 'Failed to get playlist'


# add user -> get user and validate it is exist
def test_get_user_not_exist(json_config):
    user = tests_logic.build_user_dictionary('user_not_exist', '123456')
    res = request_actions.get_user(user)
    assert tests_logic.found_error(res, 'user ' + user['user_name'] + ' does not exist'), 'Error not found, but expected'


@pytest.mark.xfail
def test_get_song_not_exist(json_config):
    song = tests_logic.build_song_dictionary('aaa', '1989', 'bruaace', 'love_aaaato_rock2')

    res = request_actions.get_song(song['song_title'])
    assert tests_logic.found_error(res, 'this song does not exist'), 'Error not found, but expected'


def test_get_playlist_not_exist(json_config):
    user = json_config['users'][1]
    playlist = tests_logic.build_playlist_dictionary('not_exist_playlist')
    res = request_actions.get_playlist(user, playlist['playlist_name'])
    assert not tests_logic.found_error(res), 'could not add playlist'


#freind is been added even if its not an exist user
def test_add_friend_not_exist(json_config):
    userA = json_config['users'][1]
    userB = tests_logic.build_user_dictionary('user_not_exist', 'pppppp')
    res = request_actions.add_friend(userA, userB)
    assert tests_logic.found_error(res), 'expected to find error'


def test_add_not_exist_song_to_playlist(json_config):
    song = tests_logic.build_song_dictionary('rock', '1989', 'bruce', 'love_to_rock2')
    user = json_config['users'][3]
    pl = json_config['playlists'][3]

    request_actions.add_playlist(user, pl)
    res = request_actions.add_song_to_playlist(user, pl, song)
    assert tests_logic.found_error(res), 'expected error, but not found'


def test_downvote_zero_ranked_song(json_config):
    user = json_config['users'][2]
    song = json_config['songs'][2]
    pl = json_config['playlists'][2]

    res = request_actions.get_playlist(user, pl['playlist_name'])
    assert tests_logic.get_rank(res, song) == 0, 'expected rating to be zero by default'
    res = request_actions.song_downvote(user, pl, song)
    res = request_actions.get_playlist(user, pl['playlist_name'])
    assert tests_logic.get_rank(res, song) == 0, 'expected rating to be stay zero if downvoating a song that is already zero'