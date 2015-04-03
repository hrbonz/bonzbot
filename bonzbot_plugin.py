# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot

    @irc3.event(r':(?P<ns>\w+)!NickServ@services. NOTICE (?P<nick>.*) :'
        r'This nickname is registered.*')
    def identify(self, ns=None, nick=None):
        try:
            password = self.bot.config['nickserv_pwd']
        except KeyError:
            pass
        else:
            self.bot.privmsg(ns, 'identify %s %s' % (nick, password))

    @irc3.event(r':(?P<ns>\w+)!NickServ@services. NOTICE (?P<nick>.*) :'
        r'You are now identified for ')
    def join_r_channels(self, ns=None, nick=None):
        self.bot.join(self.bot.config['invite_channel'])
