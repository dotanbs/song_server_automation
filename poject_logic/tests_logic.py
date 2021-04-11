from poject_logic import request_actions


def found_error(res, expected_error=None):
    if 'error' in res:
        if expected_error is not None:
            if expected_error in res['error']:
                return True
            else:
                print('expected error: ' + expected_error + ' ,while actual error: ' + res['error'])
                return False
        print('Error: ' + res['error'])
        return True
    else:
        print('Found no errors')
        return False


def validate_key_value(res, key, value):
    validated = False
    if 'data' in res:
        if isinstance(res['data'], list):
            for i in res['data']:
                for k, v in i.items():
                    if k == key and v == value:
                        validated = True
            if validated:
                return True
        else:
            for k, v in res['data'].items():
                if k == key:
                    if value == value:
                        return True
                    else:
                        return False
            return False
    print('no data in response')
    return False


def validate_song_is_in_playlist(res, song_name):
    song = get_dictionary(res, 'title', song_name)
    if song is not None and song['title'] == song_name:
        return True


def get_dictionary(res, key, value):
    if 'data' in res:
        if isinstance(res['data'], list):
            for i in res['data']:
                for k, v in i.items():
                    if k == key and v == value:
                        return i
        else:
            for k, v in res['data'].items():
                if k == key:
                    if value == value:
                        return res['data']


def validate_user_exist(res, user):
    return validate_key_value(res, 'user_name', user)


def validate_song_exist(res, song_name):
    return validate_key_value(res, 'title', song_name)


def validate_friend_exist(res, freind):
    return validate_key_value(res, 'friends', freind)


def get_rank(playlist, song_name):
    song = get_dictionary(playlist, 'title', song_name)
    return song['rating']


def create_songs_ranked():
    # add 3 users 3 songs
    # upvote 2 songs from more than one users (meaning 2 songs ranked above 1) and get song by rank
    for i in range(3):
        request_actions.add_user(f'user{i}', f'pwd{i}')
        request_actions.add_playlist(f'user{i}', f'pwd{i}', f'pl{i}')
        for j in range(3):
            request_actions.add_song('test_rank_genere', '1999', f'singer{j}', f'song_for_vote{j}')
            request_actions.add_song_to_playlist(f'user{i}', f'pwd{i}', f'pl{i}', f'song_for_vote{j}')
            if (j % 2) == 0:
                request_actions.song_upvote(f'user{i}', f'pwd{i}', f'pl{i}', f'song_for_vote{j}')
            if not (i % 2) == 0 and not (j % 2) == 0:
                request_actions.song_upvote(f'user{i}', f'pwd{i}', f'pl{i}', f'song_for_vote{j}')


def create_user_pl_song(user, pwd, pl, genere, year, performer, title):
    request_actions.add_user(user, pwd)
    request_actions.add_song(genere, year, performer, title)
    request_actions.add_playlist(user, pwd, pl)
    request_actions.add_song_to_playlist(user, pwd, pl, title)






