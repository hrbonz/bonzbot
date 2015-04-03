# -*- coding: utf-8 -*-
import irc3
from irc3 import utils


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._config = bot.config['nickserv']
        self._channels = utils.as_list(self._config['invite_channels'])

    def join(self, channels=None):
        if channels is None:
            channels = self._channels

        for channel in channels:
            channel = utils.as_channel(channel)
            self.bot.log.info('Trying to join %s', channel)
            self.bot.join(channel)

    @irc3.event(r':(?P<ns>\w+)!NickServ@services. NOTICE (?P<nick>.*) :'
        r'This nickname is registered.*')
    def identify(self, ns=None, nick=None):
        try:
            password = self._config['nickserv_pwd']
        except KeyError:
            pass
        else:
            self.bot.privmsg(ns, 'identify %s %s' % (nick, password))

    @irc3.event(r':(?P<ns>\w+)!NickServ@services. NOTICE (?P<nick>.*) :'
        r'You are now identified for ')
    def join_r_channels(self, ns=None, nick=None):
        self.join()
