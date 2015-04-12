# -*- coding: utf-8 -*-
import irc3
from irc3 import utils

__doc__ = """Freenode nickserv plugin for irc3

Here's an example of configuration for this plugin:

.. code-block:: ini

    [nickserv]
    pwd_file = nickserv_pwd.txt
    r_channels = #bonz


Options are:

* ``pwd_file``: a file containing the password for nickserv, this is a
  path relative to the plugin folder. Default value is
  'nickserv_pwd.txt'
* ``r_channels``: list of channels that require a nickname to be
  registered. Those channels will be joined automatically after a
  successful identification to nickserv.
"""


PWD_FILE = 'nickserv_pwd.txt'


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._config = bot.config['nickserv']
        self._channels = utils.as_list(self._config['r_channels'])
        self._nickserv_pwd = None
        pwd_file = 'pwd_file' in self._config \
            and self._config['pwd_file'] or PWD_FILE
        try:
            self._nickserv_pwd = open(pwd_file, 'r').read().rstrip()
        except IOError:
            self.bot.log.error("[nickserv] no such password file "
                "({})".format(pwd_file))

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
        if self._nickserv_pwd is None:
            self.bot.log.info("[nickserv] no password set")
            return
        pwd = self._nickserv_pwd
        self.bot.privmsg(ns, 'identify %s %s' % (nick, pwd))
        self.bot.log.info('Identification as {} requested'.format(nick))

    @irc3.event(r':(?P<ns>\w+)!NickServ@services. NOTICE (?P<nick>.*) :'
        r'You are now identified for ')
    def join_r_channels(self, ns=None, nick=None):
        self.bot.log.info('Identification as {} successful'.format(nick))
        self.join()
