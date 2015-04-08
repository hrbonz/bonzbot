# -*- coding: utf-8 -*-
import re
import urllib2

import bs4
import irc3
from irc3 import rfc, utils


LINK_RE = re.compile(r'(https?://[^ ]+)', re.MULTILINE|re.UNICODE)

@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._channels = utils.as_list(
            self.bot.config['linktitles']['echo_channels'])

    def get_title(self, link):
        try:
            req = urllib2.Request(link,
                headers={"Accept-Language" : "fr-FR, fr, en"})
            soup = bs4.BeautifulSoup(urllib2.urlopen(req, timeout=5))
        except urllib2.HTTPError as e:
            self.bot.log.info("linktitles: {} ({})".format(
                req.get_full_url(), e.code))
            return None
        if soup.title is not None:
            return soup.title.string

    def echo(self, target, data):
        target = utils.as_channel(target)
        self.bot.privmsg(target, "linktitle: {}".format(data))

    @irc3.event(rfc.PRIVMSG)
    def getlink(self, mask=None, event=None, target=None, data=None):
        if target in self._channels:
            matches = LINK_RE.findall(data)
            if matches is not None:
                for match in matches:
                    title = self.get_title(match)
                    if title:
                        self.echo(target, title)
