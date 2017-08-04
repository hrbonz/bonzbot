# -*- coding: utf-8 -*-
import json
import re
try:
    # python 3.x
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
except ImportError:
    # python 2.x
    from urllib2 import Request, urlopen, HTTPError

import bs4


def wikipedia_info(match):
    data = wikipedia_api("https://{}.wikipedia.org/w/api.php?format=json"
            "&action=query&prop=extracts&titles={}&exintro=&explaintext="
            "&exsentences=2&formatversion=2".format(
            match.group("lang"), match.group("page")))
    # FIXME(hr): split the text so everything gets through. There's a
    # pyload size limitation when sending a message
    return "{} [...]".format(data["query"]["pages"][0]["extract"])

def wikipedia_api(link):
    try:
        req = Request(link)
        res = urlopen(req, timeout=5)
    except HTTPError as e:
        print(u"linkinfo: {} ({})".format(
            req.get_full_url(), e.code))
        return None
    return json.loads(res.read().decode("utf-8"))


INTENTS = [
    (re.compile(r'https?://(?P<lang>.+)\.wikipedia\.org/wiki/(?P<page>.+)', re.MULTILINE|re.UNICODE),
     wikipedia_info)
]
