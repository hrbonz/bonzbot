# -*- coding: utf-8 -*-
import re
import urllib2
import pkgutil

import bs4
import irc3
from irc3 import rfc, utils


LINK_RE = re.compile(r'(https?://[^ ]+)', re.MULTILINE|re.UNICODE)


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._channels = utils.as_list(
            self.bot.config['linkinfo']['echo_channels'])
        self._intents = []
        for importer, modname, ispkg in pkgutil.iter_modules(__path__):
            mod = importer.find_module(modname).load_module(modname)
            self._intents.extend(mod.INTENTS)
        self._intents.append((LINK_RE, self.get_title))

    def get_title(self, match):
        link = match.group(1)
        try:
            req = urllib2.Request(link,
                headers={"Accept-Language": "fr-FR, fr, en"})
            soup = bs4.BeautifulSoup(urllib2.urlopen(req, timeout=5))
        except urllib2.HTTPError as e:
            self.bot.log.error(u"linkinfo: {} ({})".format(
                req.get_full_url(), e.code))
            return None
        if soup.title is not None:
            return " ".join(soup.title.string.split())

    def echo(self, target, data):
        target = utils.as_channel(target)
        self.bot.privmsg(target, u"linkinfo: {}".format(data))

    def get_info(self, link):
        for (_re, _handler) in self._intents:
            match = _re.match(link)
            if match is not None:
                self.bot.log.debug(u"linkinfo: {}".format(_re.pattern))
                return _handler(match)
        self.bot.log.debug(u"linkinfo: no intent ({})".format(link))
        return None

    @irc3.event(rfc.PRIVMSG)
    def getlink(self, mask=None, event=None, target=None, data=None):
        if target in self._channels:
            links = LINK_RE.findall(data)
            if links is not None:
                for link in links:
                    info = self.get_info(link)
                    if info:
                        self.echo(target, info)
