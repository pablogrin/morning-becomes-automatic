import json
import requests
from datetime import datetime, timedelta
from dateutil import tz

base_url = "https://tracklist-api.kcrw.com/Simulcast/date/{year}/{month}/{day}"
track_id_field = "spotify_id"
track_search_field = "affiliateLinkSpotify"
search_prefix = "spotify:search:"
episode_timezone = tz.gettz('America/Los_Angeles')


def get_last_episode_date():
    now = datetime.now(episode_timezone)
    today = now.date()
    today_weekday = today.weekday()
    episode_upload = datetime(today.year, today.month, today.day,
                              12, 0, 0, 0, episode_timezone)

    if today_weekday in [1, 2, 3, 4] and now < episode_upload:
        today = today - timedelta(days=1)
    if today_weekday == 5:
        today = today - timedelta(days=1)
    if today_weekday == 6:
        today = today - timedelta(days=2)
    if today_weekday == 0 and now < episode_upload:
        today = today - timedelta(days=3)
    return today


def get_tracklist(date, logger):
    logger.debug("Getting tracklist for date {}".format(date))
    url = base_url.format(year=date.year, month=date.month, day=date.day)
    response = requests.get(url, params={"time": "09:00", "on_demand": "1"})
    parsed = parse_response(response)
    logger.debug("Got {} tracks from {} tracklist".format(len(parsed), date))
    return parsed


def parse_response(response):
    tracks = json.loads(response.content)
    track_info = []
    for t in tracks:
        track_info.append((t[track_id_field], t[track_search_field]))

    filtered_tracks = list(filter(lambda ti: ti[1] is not None, track_info))

    return list(map(lambda ft: (ft[0], ft[1].replace(search_prefix, "")), filtered_tracks))
