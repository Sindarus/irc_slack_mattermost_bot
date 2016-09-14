#!/usr/bin/env python2
# -*- coding: utf8 -*-

# In this simple script, there are global variables : my_ircbot
# and my_slackbot, that are instances of IrcBot and SlackBot.
# Each bot runs in a separate thread.
# Another global variable is table, which tells how channels should be linked
# together, it is needed for every bot to know on which channels to connect and
# stuff like that.

import central_unit

central_unit.start()
