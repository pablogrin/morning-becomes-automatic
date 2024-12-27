import os
import logging
from helpers.kcrw_helper import get_last_episode_date, get_tracklist
from helpers.spotify_helper import get_user_data, get_tracks_ids, update_playlist

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

def run():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    date = get_last_episode_date()
    logger.info('Started process for {}'.format(date))
    tracklist = get_tracklist(date, logger)
    spotify_client, spotify_user_id = get_user_data()
    tracks = get_tracks_ids(spotify_client, tracklist, logger)
    update_playlist(spotify_client, spotify_user_id, tracks, logger)
    logger.info('Ended process for {}'.format(date))


def handler(event, context):
    run()


if __name__ == '__main__':
    run()
