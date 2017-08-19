# -*- coding: utf-8 -*-
import os.path
import pkgutil
import re
import sys

import irc3

from .utils import get_title, split_msg
from .github import INTENTS as github_intents
from .wikipedia import INTENTS as wikipedia_intents


LINK_RE = re.compile(r'(https?://[^ ]+)', re.MULTILINE|re.UNICODE)


@irc3.plugin
class LinkinfoPlugin(object):

    intents = []

    def __init__(self, bot):
        self.bot = bot
        self._channels = irc3.utils.as_list(
            self.bot.config['linkinfo']['channels'])
        if 'enabled' in self.bot.config['linkinfo']:
            heremod = sys.modules[__name__]
            for modname in irc3.utils.as_list(
                    self.bot.config['linkinfo']['enabled']):
                intents = getattr(heremod, "{}_intents".format(modname))
                self.intents.extend(intents)
        self.intents.append((LINK_RE, self.get_title))

    def get_title(self, match):
        """Default action when no other intent is found"""
        link = match.group(1)
        return get_title(link)

    def echo(self, target, data):
        target = irc3.utils.as_channel(target)
        msgs = split_msg(u"linkinfo: {}".format(data))
        for msg in msgs:
            self.bot.privmsg(target, msg)

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
