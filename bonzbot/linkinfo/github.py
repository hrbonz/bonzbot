# -*- coding: utf-8 -*-
import json
import re

from .utils import get_title, get_uri


def github_info(match, config):
    api_data = github_api('/repos/{}/{}'.format(
        match.group('owner'), match.group('repo')))
    title = get_title(match.string)
    return "{title} ({lang})".format(
        title=title,
        lang=api_data['language'],
    )

def github_api(link):
    res = get_uri('https://api.github.com' + link,
            headers={'Accept': 'application/vnd.github.v3+json'})
    return json.loads(res.read().decode("utf-8"))


INTENTS = [
    (re.compile(r'https?://github.com/(?P<owner>[^\/]+)/(?P<repo>[^\/]+)', re.MULTILINE|re.UNICODE),
     github_info)
]
