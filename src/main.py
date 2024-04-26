from datetime import date
from helpers.kcrw_helper import get_tracklist
from helpers.spotify_helper import get_user_data, search_tracks, update_playlist

if __name__ == '__main__':
    today = date.today()

    if today.weekday() < 5:
        tracklist = get_tracklist(today)
        spotify_client, spotify_user_id = get_user_data()
        tracks = search_tracks(spotify_client, tracklist)
        update_playlist(spotify_client, spotify_user_id, tracks)
