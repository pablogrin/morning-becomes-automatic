import json
import requests

base_url = "https://tracklist-api.kcrw.com/Simulcast/date/{year}/{month}/{day}"
track_id_field = "spotify_id"
track_search_field = "affiliateLinkSpotify"
search_prefix = "spotify:search:"


def get_tracklist(date):
    url = base_url.format(year=date.year, month=date.month, day=date.day)
    response = requests.get(url, params={"time": "09:00", "on_demand": "1"})
    return parse_response(response)


def parse_response(response):
    tracks = json.loads(response.content)
    track_info = []
    for t in tracks:
        track_info.append((t[track_id_field], t[track_search_field]))

    filtered_tracks = list(filter(lambda ti: ti[1] is not None, track_info))

    return list(map(lambda ft: (ft[0], ft[1].replace(search_prefix, "")), filtered_tracks))
