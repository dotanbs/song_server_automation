def found_error(res, expected_error=None):
    if 'error' in res:
        if expected_error is not None:
            if res['error'] is expected_error:
                return True
            else:
                print('expected error: ' + expected_error + ' ,while actual error: ' + res['error'])
                return False
        return True
    else:
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


def build_song_object(song_genre, song_year, song_performer, song_title):
    song = {'song_genre': song_genre, 'song_year': song_year, 'song_performer': song_performer,
            'song_title': song_title}
    return song



