import rest_sender.send as send


def add_user(user, pwd):
    body = {'user_name': user, 'user_password': pwd}
    res = send.post("users/add_user", body)


def get_user(user):
    return send.get("users/get_user?user_name=" + user)


def add_friend(user, pwd, friend):
    body = {'user_name': user, 'user_password': pwd, 'friend_name': friend}
    send.put("users/add_friend", body)


def add_playlist(user, pwd, playlist_name):
    body = {'user_name': user, 'user_password': pwd, 'playlist_name': playlist_name}
    return send.post("users/add_playlist", body)


def add_song(song_genre, song_year, song_performer, song_title):
    body = {'song_genre': song_genre, 'song_year': song_year, 'song_performer': song_performer,
            'song_title': song_title}
    return send.post("songs/add_song", body)


def get_song(song_title):
    return send.get("songs/get_song?song_title=" + song_title)


def song_upvote(user, pwd, playlist_name, song_title):
    body = {'user_name': user, 'user_password': pwd, 'playlist_name': playlist_name, 'song_title': song_title}
    return send.put("users/upvote", body)


def song_downvote(user, pwd, playlist_name, song_title):
    body = {'user_name': user, 'user_password': pwd, 'playlist_name': playlist_name, 'song_title': song_title}
    return send.put("users/downvote", body)


def add_song_to_playlist(user, pwd, playlist_name, song_title):
    body = {'user_name': user, 'user_password': pwd, 'playlist_name': playlist_name, 'song_title': song_title}
    return send.post("playlists/add_song", body)


def get_playlist(user, pwd, playlist_name):
    return send.get(
        "users/get_playlist?user_name=" + user + '&user_password=' + pwd + '&playlist_name=' + playlist_name)


def get_song_by_rank(rank, op):
    return send.get(
        "songs/ranked_songs?rank=" + rank + '&op=' + op)


def change_password(user, old_password, new_password):
    body = {'user_name': user, 'user_password': old_password, 'user_new_password': new_password}
    return send.put("users/change_password", body)


def delete_all_users():
    return send.delete("admin/delete_all_users")


def delete_all_songs():
    return send.delete("admin/delete_all_songs")


def set_songs_into_db(songs_list):
    return send.post("admin/set_songs", songs_list)


def set_users_into_db(users_list):
    return send.post("admin/set_users", users_list)
