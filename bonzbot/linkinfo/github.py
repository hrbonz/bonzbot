# -*- coding: utf-8 -*-
import json
import re
import urllib2


def github_info(match):
    res = github_api('/repos/{}/{}'.format(
        match.group('owner'), match.group('repo')))
    return "{desc} ({lang})".format(
        desc=res['description'],
        lang=res['language'],
    )

def github_api(link):
    try:
        req = urllib2.Request('https://api.github.com' + link,
            headers={'Accept': 'application/vnd.github.v3+json'})
        res = urllib2.urlopen(req, timeout=5)
    except urllib2.HTTPError as e:
        print(u"linkinfo: {} ({})".format(
            req.get_full_url(), e.code))
        return None
    return json.load(res)

INTENTS = [
    (re.compile(r'https?://github.com/(?P<owner>[^ ]+)/(?P<repo>[^ ]+)', re.MULTILINE|re.UNICODE),
     github_info)
]
