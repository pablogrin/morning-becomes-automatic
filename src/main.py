from helpers.kcrw_helper import get_last_episode_date, get_tracklist
from helpers.spotify_helper import get_user_data, get_tracks_ids, update_playlist

if __name__ == '__main__':

    date = get_last_episode_date()
    tracklist = get_tracklist(date)
    spotify_client, spotify_user_id = get_user_data()
    tracks = get_tracks_ids(spotify_client, tracklist)
    update_playlist(spotify_client, spotify_user_id, tracks)
