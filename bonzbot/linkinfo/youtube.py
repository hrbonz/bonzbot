# -*- coding: utf-8 -*-
import json
import re

from .utils import get_uri


def youtube_info(match, config):
    apikey_file = config["youtube_apikey"]
    # FIXME(hr): clean failover when file not found
    with open(apikey_file, "r") as apikey_fd:
        apikey = apikey_fd.read().strip()

    data = youtube_api("https://www.googleapis.com/youtube/v3/videos?"
            "key={apikey}&part=snippet&id={vidid}".format(
            apikey=apikey, vidid=match.group("vidid")))

    if len(data["items"]) != 0:
        return data["items"][0]["snippet"]["title"]
    else:
        return "Unknown video"

def youtube_api(link):
    res = get_uri(link)
    return json.loads(res.read().decode("utf-8"))


INTENTS = [
    (re.compile(r'https?://www\.youtube\.com/.*v=(?P<vidid>\w+)\&?', re.MULTILINE|re.UNICODE),
     youtube_info),
    (re.compile(r'https?://youtu\.be/(?P<vidid>\w+)\??', re.MULTILINE|re.UNICODE),
     youtube_info),
]
