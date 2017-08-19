# -*- coding: utf-8 -*-
import json
import re

from .utils import get_uri


def wikipedia_info(match):
    data = wikipedia_api("https://{}.wikipedia.org/w/api.php?format=json"
            "&action=query&prop=extracts&titles={}&exintro=&explaintext="
            "&exsentences=4&formatversion=2".format(
            match.group("lang"), match.group("page")))
    # FIXME(hr): split the text so everything gets through. There's a
    # pyload size limitation when sending a message
    return "{} [...]".format(data["query"]["pages"][0]["extract"])

def wikipedia_api(link):
    res = get_uri(link)
    return json.loads(res.read().decode("utf-8"))


INTENTS = [
    (re.compile(r'https?://(?P<lang>.+)\.wikipedia\.org/wiki/(?P<page>.+)', re.MULTILINE|re.UNICODE),
     wikipedia_info)
]
