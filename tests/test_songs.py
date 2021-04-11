from poject_logic import request_actions, tests_logic
import pytest


# add user -> get user and validate it is exist
def test_add_user():
    res = request_actions.add_user('dotan', '123456')
    assert not tests_logic.found_error(res), 'Failed to add user: dotan'

    res = request_actions.get_user('dotan')
    assert tests_logic.validate_user_exist(res, 'dotan'), 'user \'dotan\' not found'


# add user -> get user and validate it is exist
def test_add_user_that_already_exist():
    res = request_actions.add_user('dotan', '123456')
    assert not tests_logic.found_error(res), 'Failed to add user: \'dotan\''

    res = request_actions.add_user('dotan', 'pwd')
    assert tests_logic.found_error(res), 'expected to found error that user already exist'


@pytest.mark.parametrize('rank, op, expected',
                         [('0', 'greater', ['song_for_vote0', 'song_for_vote1', 'song_for_vote2']),
                          ('2', 'less', ['song_for_vote1']),
                          ('3', 'eq', ['song_for_vote0', 'song_for_vote2'])])
def test_get_song_by_rank(rank, op, expected):
    tests_logic.create_songs_ranked()
    # song_for_vote0 rank = 3, song_for_vote2 rank = 3, song_for_vote1 rank = 1
    res = request_actions.get_song_by_rank(rank, op)
    assert res['data'] == expected


# run add song and validate there are no errors and that the song exist
def test_add_song():
    res_add_song = request_actions.add_song('rock', '1989', 'bruce', 'love_to_rock2')
    assert not tests_logic.found_error(res_add_song), 'Failed to add song'
    res_get_song = request_actions.get_song('love_to_rock2')
    assert tests_logic.validate_song_exist(res_get_song, 'love_to_rock2')


# add a playlist to a preconfigured user from tearup and make sure it was added
def test_add_playlist():
    request_actions.add_user('user_add_pl', 'pwd_add_pl')
    res1 = request_actions.add_playlist('user_add_pl', 'pwd_add_pl', 'playlist1')
    assert not tests_logic.found_error(res1), 'could not add playlist'

    res = request_actions.get_playlist('user_add_pl', 'pwd_add_pl', 'playlist2')
    assert not tests_logic.found_error(res), 'could not add playlist'


# add a playlist to a preconfigured user from tearup and make sure it was added
def test_add_multiple_playlist():
    res = request_actions.add_user('user1', '555555')
    for i in range(3):
        request_actions.add_playlist('user1', '555555', f'pl{i}')

    for i in range(3):
        request_actions.add_playlist('user1', '555555', f'pl{i}')
        res = request_actions.get_playlist('user1', '555555', f'pl{i}')
        assert not tests_logic.found_error(res), 'could not get playlist: ' + f'pl{i}'


# add same playlist name to 2 different users
def test_add_multiple_users_same_playlist_name():
    for i in range(3):
        request_actions.add_user(f'user{i}', f'pwd{i}')
        request_actions.add_playlist(f'user{i}', f'pwd{i}', 'pl_same')
    for i in range(3):
        res = request_actions.get_playlist(f'user{i}', f'pwd{i}', 'pl_same')
        assert not tests_logic.found_error(res), 'playlist \'pl_same\' not fond or failed to get playlist'


# add a playlist and a song and validate it is now in the song
def test_add_song_to_playlist():
    request_actions.add_user('user_add_song_to_playist', '111111')
    request_actions.add_song('song_1', '1989', 'bruce', 'song_topl1')

    res = request_actions.add_playlist('user_add_song_to_playist', '111111', 'pl1')
    assert not tests_logic.found_error(res), 'could not add playlist'

    res = request_actions.add_song_to_playlist('user_add_song_to_playist', '111111', 'pl1',
                                               'song_topl1')
    assert not tests_logic.found_error(res), 'could not add song to playlist'

    res = request_actions.get_playlist('user_add_song_to_playist', '111111', 'pl1')
    assert tests_logic.validate_song_exist(res, 'song_topl1')


# add a playlist and a multiple songs song and validate it is now in the playlist
def test_add_multiple_songs_to_playlist():
    request_actions.add_user('user_with_multiple_songs', '111111')
    request_actions.add_playlist('user_with_multiple_songs', '111111', 'playlist_multiple_songs')
    for i in range(3):
        request_actions.add_song(f'song_{i}', '1989', f'singer{i}', f'song_topl{i}')
        request_actions.add_song_to_playlist('user_with_multiple_songs', '111111', 'playlist_multiple_songs',
                                             f'song_topl{i}')

    res = request_actions.get_playlist('user_with_multiple_songs', '111111', 'playlist_multiple_songs')
    for i in range(3):
        assert tests_logic.validate_song_exist(res, f'song_topl{i}')


# take 2 users from config and add userB to userA
def test_add_friend():
    request_actions.add_user('userA', 'pwdA')
    request_actions.add_user('userB', 'pwdB')

    request_actions.add_friend('userA', 'pwdA', 'pwdB')
    res = request_actions.get_user('userA')
    assert tests_logic.validate_friend_exist(res, 'userB'), 'userB was not found in the friends list'

    res = request_actions.get_user('userB')
    assert tests_logic.validate_friend_exist(res, 'userA'), 'userA was not found in the friends list'


def test_upvote_song():
    tests_logic.create_user_pl_song('uservote', 'pwdVote', 'pl_for_vote', 'song_for_vote', '1989', 'singer',
                                    'song_for_vote_title')

    pl_res = request_actions.get_playlist('uservote', 'pwdVote', 'pl_for_vote')
    rank_before_upvote = tests_logic.get_rank(pl_res, 'song_for_vote_title')
    request_actions.song_upvote('uservote', 'pwdVote', 'pl_for_vote', 'song_for_vote_title')
    res = request_actions.get_playlist('uservote', 'pwdVote', 'pl_for_vote')
    rank_after_upvote = tests_logic.get_rank(res, 'song_for_vote_title')
    assert rank_after_upvote is (rank_before_upvote + 1)


def test_downvote_song():
    tests_logic.create_user_pl_song('userDownvote', 'pwdDownVote', 'pl_for_downvote', 'song_for_Downvote', '1989',
                                    'singer', 'song_for_downvote_title')

    res_get_pl_rank0 = request_actions.get_playlist('userDownvote', 'pwdDownVote', 'pl_for_downvote')
    rank_before_upvote = tests_logic.get_rank(res_get_pl_rank0, 'song_for_downvote_title')

    request_actions.song_upvote('userDownvote', 'pwdDownVote', 'pl_for_downvote', 'song_for_downvote_title')

    request_actions.song_downvote('userDownvote', 'pwdDownVote', 'pl_for_downvote', 'song_for_downvote_title')
    res_get_pl_after_downvote = request_actions.get_playlist('userDownvote', 'pwdDownVote', 'pl_for_downvote')
    rank_after_downvote = tests_logic.get_rank(res_get_pl_after_downvote, 'song_for_downvote_title')

    assert rank_before_upvote is rank_after_downvote


def test_change_password():
    request_actions.add_user('user_for_change_pwd', 'orig_pwd')
    request_actions.add_playlist('user_for_change_pwd', 'orig_pwd', 'pl_to_change_pwd')
    new_password = 'new_pwd'

    request_actions.change_password('user_for_change_pwd', 'orig_pwd', new_password)
    res_for_old_pwd = request_actions.get_playlist('user_for_change_pwd', 'orig_pwd', 'pl_to_change_pwd')
    assert tests_logic.found_error(res_for_old_pwd), 'found no error, but expected error for incorrect pwd'

    res_get_pl_new_pwd = request_actions.get_playlist('user_for_change_pwd', new_password, 'pl_to_change_pwd')
    assert not tests_logic.found_error(res_get_pl_new_pwd), 'Failed to get playlist with the new password'


# add user -> get user and validate it is exist
def test_get_user_not_exist():
    res = request_actions.get_user('user_not_exist')
    assert tests_logic.found_error(res, 'user ' + 'user_not_exist' + ' does not exist'), 'Error not found, but expected'


@pytest.mark.xfail
def test_get_song_not_exist():
    res = request_actions.get_song('song_does_not_exist')
    assert tests_logic.found_error(res, 'this song does not exist'), 'expect to find error for song does not exist'


def test_get_playlist_not_exist():
    request_actions.add_user('user', 'pwd')
    res = request_actions.get_playlist('user', 'pwd', 'not_exist_playlist')
    assert not tests_logic.found_error(res), 'expected to find error for playlist does not exist, but no error found'


# freind is been added even if its not an exist user
def test_add_friend_not_exist():
    request_actions.add_user('user', 'pwd')
    res = request_actions.add_friend('user', 'pwd', 'user_not_exist')
    assert tests_logic.found_error(res), 'expected to find error for user does not exist, but no error found'


def test_add_not_exist_song_to_playlist():
    request_actions.add_user('user', 'pwd')
    request_actions.add_playlist('user', 'pwd', 'pl')
    res = request_actions.add_song_to_playlist('user', 'pwd', 'pl', 'not_exist_song')
    assert tests_logic.found_error(res), 'expected to find error for song does not exist, but no error found'


def test_downvote_zero_ranked_song():
    tests_logic.create_user_pl_song('userDownvoteZero', 'pwdDownVote', 'pl_for_downvote', 'song_for_DownvoteZero',
                                    '1989', 'singer', 'song_for_downvoteZero_title')

    res = request_actions.get_playlist('userDownvoteZero', 'pwdDownVote', 'pl_for_downvote')
    assert tests_logic.get_rank(res, 'song_for_downvoteZero_title') == 0, 'expected rating to be zero by default'

    res = request_actions.song_downvote('userDownvoteZero', 'pwdDownVote', 'pl_for_downvote',
                                        'song_for_downvoteZero_title')
    res = request_actions.get_playlist('userDownvoteZero', 'pwdDownVote', 'pl_for_downvote')
    assert tests_logic.get_rank(res,
                                'song_for_downvoteZero_title') == 0, 'expected rating to be zero if downvoating a song that is already zero'
