# -*- coding: utf-8 -*-
import random
import re

import irc3

import praw
from prawcore.exceptions import ServerError


__doc__ = """
Good bot plugin for irc3
========================

This plugin answers various messages sent directly or indirectly to the
bot.

Configuration
-------------

.. code-block:: ini

    [goodbot]
    channels = #bonz

Options are:

* ``channels``: space separated list of channels where the bot
  should listen for messages
"""

# TODO(hr): move to settings
stems = [
    {
        "trigger": re.compile(r"good bot"),
        "answers": ["blip blup", "/me blushes", "Oh you, you're too much"],
    }
]


@irc3.plugin
class GoodBotPlugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._channels = irc3.utils.as_list(
            self.bot.config['goodbot']['channels'])

    @irc3.event(irc3.rfc.PRIVMSG)
    def listen(self, mask=None, event=None, target=None, data=None):
        if target not in self._channels:
            return

        for stem in stems:
            match = stem["trigger"].search(data)
            if match:
                self.bot.privmsg(target, random.choice(stem["answers"]))
