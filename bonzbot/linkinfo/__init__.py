# -*- coding: utf-8 -*-
import os.path
import pkgutil
import re
try:
    # python 3.x
    from urllib.request import Request, urlopen
except ImportError:
    # python 2.x
    from urllib2 import Request, urlopen

import bs4
import irc3


LINK_RE = re.compile(r'(https?://[^ ]+)', re.MULTILINE|re.UNICODE)


@irc3.plugin
class LinkinfoPlugin(object):

    intents = []

    def __init__(self, bot):
        self.bot = bot
        self._channels = irc3.utils.as_list(
            self.bot.config['linkinfo']['channels'])
        herepath = os.path.dirname(__file__)
        for importer, modname, ispkg in pkgutil.iter_modules([herepath, ]):
            mod = importer.find_module(modname).load_module(modname)
            self.intents.extend(mod.INTENTS)
            self.bot.log.debug(u"linkinfo: add {}".format(modname))
        self.intents.append((LINK_RE, self.get_title))

    def get_title(self, match):
        """Default action when no other intent is found"""
        link = match.group(1)
        try:
            req = Request(link,
                headers={"Accept-Language": "fr-FR, fr, en"})
            soup = bs4.BeautifulSoup(urlopen(req, timeout=5), "lxml")
        except urllib2.HTTPError as e:
            self.bot.log.error(u"linkinfo: {} ({})".format(
                req.get_full_url(), e.code))
            return None
        if soup.title is not None:
            return " ".join(soup.title.string.split())

    def echo(self, target, data):
        target = irc3.utils.as_channel(target)
        self.bot.privmsg(target, u"linkinfo: {}".format(data))

    def get_info(self, link):
        for (_re, _handler) in self.intents:
            match = _re.match(link)
            if match is not None:
                self.bot.log.debug(u"linkinfo: {}".format(_re.pattern))
                return _handler(match)
        self.bot.log.debug(u"linkinfo: no intent ({})".format(link))
        return None

    @irc3.event(irc3.rfc.PRIVMSG)
    def getlink(self, mask=None, event=None, target=None, data=None):
        if target in self._channels:
            links = LINK_RE.findall(data)
            if links is not None:
                for link in links:
                    info = self.get_info(link)
                    if info:
                        self.echo(target, info)
