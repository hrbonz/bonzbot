# -*- coding: utf-8 -*-
try:
    # python 3.x
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
except ImportError:
    # python 2.x
    from urllib2 import Request, urlopen, HTTPError

import bs4


UA = "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
MSG_SIZE_LIMIT = 400


def get_uri(link, headers=None):
    _headers = {
        "Accept-Language": "fr-FR, fr, en",
        "User-Agent": UA,
    }

    if headers is not None:
        _headers.update(headers)

    try:
        req = Request(link, headers=_headers)
        res = urlopen(req, timeout=5)
    except HTTPError as e:
        self.bot.log.error(u"linkinfo: {} ({})".format(
            req.get_full_url(), e.code))
        return None
    return res

def get_title(link):
    res = get_uri(link)
    if res is None:
        return None
    soup = bs4.BeautifulSoup(res, "lxml")
    if soup.title is not None:
        return " ".join(soup.title.string.split())

def split_msg(text):
    """Split text in messages of full sentences of max size
    MSG_SIZE_LIMIT
    """
    chunks = []
    chunk = ""
    for sentence in text.split(". "):
        print(sentence)
        if len(chunk) == 0:
            chunk = sentence
        elif len(chunk) + len(sentence) <= MSG_SIZE_LIMIT:
            chunk = ". ".join([chunk, sentence])
        else:
            chunk += "."
            chunks.append(chunk.strip())
            chunk = sentence
    chunks.append(chunk)
    return chunks
