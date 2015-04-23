# -*- coding: utf-8 -*-
import irc3
from irc3 import rfc, utils

import re


__doc__ = """autodeop plugin for irc3

A bot should never be op.

Here's an example of configuration for this plugin:

.. code-block:: ini

    [autodeop]
    channels = #bonz


Options are:

* ``channels``: list of channels where the bot should not be op. If no
  channel is listed, then bot will deop himself from all chans.
"""

OP_RE = re.compile(r'\+.*o')


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._channels = None
        if 'autodeop' in bot.config \
            and 'channels' in bot.config['autodeop']:
            self._channels = utils.as_list(bot.config['autodeop']['channels'])

    @irc3.event(rfc.MODE)
    def deop(self, mask=None, event=None, target=None, modes=None, data=None):
        if OP_RE.match(modes) and \
            (self._channels is None or target in self._channels):
            self.bot.mode(target, '-o', self.bot.nick)
