import json
import requests

base_url = "https://tracklist-api.kcrw.com/Simulcast/date/{year}/{month}/{day}"
track_field = "affiliateLinkSpotify"
search_prefix = "spotify:search:"


def get_tracklist(date):
    url = base_url.format(year=date.year, month=date.month, day=date.day)
    response = requests.get(url, params={"time": "09:00", "on_demand": "1"})
    return parse_response(response)


def parse_response(response):
    tracks = json.loads(response.content)
    search_terms = list(filter(lambda x: x is not None, map(lambda t: t[track_field], tracks)))
    return list(map(lambda st: st.replace(search_prefix, ""), search_terms))
