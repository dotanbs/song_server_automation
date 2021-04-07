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


def build_song_dictionary(song_genre, song_year, song_performer, song_title):
    song = {'song_genre': song_genre, 'song_year': song_year, 'song_performer': song_performer,
            'song_title': song_title}
    return song


def build_user_dictionary(user, pwd):
    user = {'user_name': user, 'user_password': pwd}
    return user


def build_playlist_dictionary(playlist_name):
    pl = {'playlist_name': playlist_name }
    return pl


def validate_user_exist(res, user):
    return validate_key_value(res, 'user_name', user)


def validate_song_exist(res, song):
    return validate_key_value(res, 'title', song)


def validate_friend_exist(res, user1, freind):
    return validate_key_value(res, 'friends', freind['user_name'])


def get_rank(playlist, song):
    song = get_dictionary(playlist, 'title', song['song_title'])
    return song['rating']


def create_songs_ranked(json_config):
    # add 3 users 3 songs
    # upvote 2 songs from more than one users (meaning 2 songs ranked above 1) and get song by rank
    userA = json_config['users'][0]
    userB = json_config['users'][1]
    userC = json_config['users'][2]

    songA = json_config['songs'][0]
    songB = json_config['songs'][1]
    songC = json_config['songs'][2]

    pl1 = json_config['playlists'][0]
    pl2 = json_config['playlists'][1]

    request_actions.add_playlist(userA, pl1)
    request_actions.add_playlist(userB, pl2)
    request_actions.add_playlist(userC, pl2)

    request_actions.add_song_to_playlist(userA, pl1, songA)
    request_actions.add_song_to_playlist(userB, pl1, songA)
    request_actions.add_song_to_playlist(userC, pl1, songA)

    request_actions.add_song_to_playlist(userA, pl2, songB)
    request_actions.add_song_to_playlist(userB, pl2, songB)
    request_actions.add_song_to_playlist(userC, pl2, songB)

    request_actions.add_song_to_playlist(userA, pl1, songC)
    request_actions.add_song_to_playlist(userB, pl1, songC)
    request_actions.add_song_to_playlist(userC, pl1, songC)

    request_actions.song_upvote(userA, pl1, songA)
    request_actions.song_upvote(userB, pl1, songA)
    request_actions.song_upvote(userC, pl1, songA)

    request_actions.song_upvote(userA, pl1, songB)
    request_actions.song_upvote(userB, pl1, songB)
    request_actions.song_upvote(userC, pl1, songB)

    request_actions.song_upvote(userA, pl1, songC)


def extract_songs_list(res):
    return res['data']


def compare_lists():
    pass






