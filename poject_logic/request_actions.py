import rest_sender.send as send


def add_user(body):
    return send.post("users/add_user", body)


def get_user(user):
    return send.get("users/get_user?user_name=" + user['user_name'])


def add_friend(user1, user2):
    body = {**user1, 'friend_name': user2['user_name']}
    return send.put("users/add_friend", body)


def add_playlist(user, playlist):
    body = {**user, **playlist}
    return send.post("users/add_playlist", body)


def add_song(body):
    return send.post("songs/add_song", body)


def get_song(song_title):
    return send.get("songs/get_song?song_title=" + song_title)


def song_upvote(user, playlist, song):
    body = {**user, **playlist, 'song_title': song['song_title']}
    return send.put("songs/upvote", body)


def song_downvote(user, playlist, song):
    body = {**user, **playlist, 'song_title': song['song_title']}
    return send.put("songs/downvote", body)


def add_song_to_playlist(user, playlist, song):
    body = {**user, **playlist, 'song_title': song['song_title']}
    return send.post("playlists/add_song", body)


def get_playlist(user, playlist_name):
    return send.get(
        "users/get_playlist?user_name=" + user['user_name'] + '&user_password=' + user['user_password'] + '&playlist_name=' + playlist_name)


def get_song_by_rank(rank, op):
    return send.get(
        "songs/ranked_songs?rank=" + rank + '&op=' + op)


def change_password(user, new_password):
    body = {**user, 'user_new_password': new_password}
    return send.put("users/change_password", body)


def delete_all_users():
    return send.delete("admin/delete_all_users")


def delete_all_songs():
    return send.delete("admin/delete_all_songs")


def set_songs_into_db(songs_list):
    return send.post("admin/set_songs", songs_list)


def set_users_into_db(users_list):
    return send.post("admin/set_users", users_list)
