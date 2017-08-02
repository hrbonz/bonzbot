# -*- coding: utf-8 -*-
import json
import re
try:
    # python 3.x
    from urllib.request import Request, urlopen, HTTPError
except ImportError:
    # python 2.x
    from urllib2 import Request, urlopen, HTTPError


def github_info(match):
    res = github_api('/repos/{}/{}'.format(
        match.group('owner'), match.group('repo')))
    return "{desc} ({lang})".format(
        desc=res['description'],
        lang=res['language'],
    )

def github_api(link):
    try:
        req = Request('https://api.github.com' + link,
            headers={'Accept': 'application/vnd.github.v3+json'})
        res = urlopen(req, timeout=5)
    except HTTPError as e:
        print(u"linkinfo: {} ({})".format(
            req.get_full_url(), e.code))
        return None
    return json.load(res)

INTENTS = [
    (re.compile(r'https?://github.com/(?P<owner>[^\/]+)/(?P<repo>[^\/]+)', re.MULTILINE|re.UNICODE),
     github_info)
]
