import base64
import os
import spotipy

client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
redirect_uri = os.environ["SPOTIFY_REDIRECT_URI"]
scope = "playlist-modify-public ugc-image-upload"
playlist_name = "Morning Becomes Automatic"
playlist_description = "KCRW's Morning Becomes Eclectic. Last episode's tracklist, updated daily."


def get_user_data():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                           client_secret=client_secret,
                                           redirect_uri=redirect_uri,
                                           scope=scope)
    client = spotipy.Spotify(auth_manager=sp_oauth)
    user_id = client.current_user()["id"]

    return client, user_id


def get_tracks_ids(client, tracks_info, logger):
    logger.debug("Getting tracks ids")
    ids = list(map(lambda ti: get_track_id(client, ti), tracks_info))
    logger.debug("Got {} tracks ids".format(len(ids)))
    return ids


def get_track_id(client, track_info):
    if track_info[0] is not None:
        return track_info[0]
    response = client.search(q=track_info[1], type='track', limit=1)
    tracks = response["tracks"]["items"]
    return tracks[0]["id"]


def update_playlist(client, user_id, tracks_ids, logger):
    playlist_id = get_playlist(client, user_id, logger)
    client.playlist_replace_items(playlist_id, tracks_ids)


def get_playlist(client, user_id, logger):
    lim = 50
    off = 0
    logger.debug("Getting playlists")
    response = client.current_user_playlists(limit=lim, offset=off)
    has_next = response["next"]
    user_playlists = response["items"]

    while has_next:
        response = client.current_user_playlists(limit=lim, offset=off+lim)
        user_playlists.extend(response["items"])
    logger.debug("Got {} playlists".format(len(user_playlists)))
    for up in user_playlists:
        if up["name"] == playlist_name:
            logger.debug("Found matching playlist with id {}".format(up['id']))
            return up["id"]

    new_id = create_playlist(client, user_id)
    logger.debug("Created playlist with id {}".format(new_id))
    return new_id


def create_playlist(client, user_id):
    playlist = client.user_playlist_create(user_id,
                                           name=playlist_name,
                                           description=playlist_description)
    playlist_id = playlist["id"]

    with open("static/playlist_cover.jpg", "rb") as f:
        image_b64 = base64.b64encode(f.read())
        client.playlist_upload_cover_image(playlist_id, image_b64)

    return playlist_id
