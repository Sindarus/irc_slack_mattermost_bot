#!/usr/bin/env python2
# -*- coding: utf8 -*-

#Configuration file for slack-irc-mattermost bot

from copy import deepcopy
from chan import *
import os
import json

from default_cfg import default_cfg

#Channels to twin together.
#This is a setting that MUST be specified here, and nowhere else.
#WARNING : if you want to link up a slack channel, you HAVE TO invite the slack
#bot to the channel. This can be done from the said channel on slack.
#Channel names of MM do NOT start with a #, also, you should always use lowercased channel
#names, even if there are uppercases letters on mattermost."
TWINNINGS = [
    [Chan("MM", "botwar"), Chan("IRC", "#test-ircbot"), Chan("Slack", "#bot-testing")]
    ,[Chan("MM", "strasbourg"), Chan("IRC", "#strasbourg"), Chan("Slack", "#strasbourg")]
    ,[Chan("MM", "ares"), Chan("IRC", "#ares"), Chan("Slack", "#irc")]
    ,[Chan("MM", "dailiieplanet"), Chan("IRC", "#dailiieplanet")]
]

# ==============================================================================
# CUSTOM SETTINGS
# Specify your own values here, these values will override the default ones
# that are set in default_cfg.py and will be overrided by environement variables
# that have the same name.
# It is recommanded that you do not specify your secrets here, because you could
# push them to git by mistake. It is recommanded to use environement variables
# instead.
# ==============================================================================
custom_cfg = {
    "IRCBOT_NAME" : "b"
}

# =====================================================
# DO NOT TOUCH THE REST OF THIS FILE
# This is the code that builds the final config dict
# =====================================================
cfg = deepcopy(default_cfg)

#override default_cfg with custom_cfg
for key in cfg:
    if key in custom_cfg.keys():
        cfg[key] = custom_cfg[key]

#override custom_cfg with environement variables
env = os.environ # retrieve environement variables
for key in cfg:
    if key in env.keys():
        cfg[key] = env[key]
        # env variables are string. If we're dealing with an int option,
        # we have to convert it
        if isinstance(default_cfg[key], int):
            try:
                cfg[key] = int(cfg[key])
            except Exception, e:
                print("You have set the config option " + key + " to the value " + cfg[key] + " but this value is supposed to be an int, and could not be converted to int. Got error : " + str(e))

# load MMBOT_OUTHOOK_TOKEN from json
cfg["MMBOT_OUTHOOK_TOKEN"] = json.loads(cfg["MMBOT_OUTHOOK_TOKEN"])
