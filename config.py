#!/usr/bin/env python2
# -*- coding: utf8 -*-

#Configuration file for slack-irc-mattermost bot

from chan import *
import os
import json

#channels to twin together
#WARNING : if you want to link up a slack channel, you HAVE TO invite the slack
#bot to the channel. This can be done from the said channel on slack.
#Channel names of MM do NOT start with a #, also, you should always use lowercased channel
#names, even if there are uppercases letters on mattermost."
TWINNINGS = [
    [Chan("MM", "botwar"), Chan("IRC", "#test-ircbot"), Chan("Slack", "#bot-testing")]
    #,[Chan("MM", "strasbourg"), Chan("IRC", "#strasbourg"), Chan("Slack", "#strasbourg")]
    #,[Chan("MM", "ares"), Chan("IRC", "#ares"), Chan("Slack", "#irc")]
    #,[Chan("MM", "dailliie planet"), Chan("IRC", "#ares"), Chan("Slack", "#general")]
]

# ==============================================================================
# You can override the following config by defining environement variables
# that have the same name
# ==============================================================================
cfg = {
    # level of infos that we should display :
    # 1 = fatal error
    # 2 = warning
    # 3 = info
    # 4 = info & messages
    "DEBUG_LEVEL" : 4,

    # IRC server on which to connect. This program can only track one irc server
    # at a time.
    "IRC_SERVER" : "",

    # port of the IRC server on which to connect
    "IRC_PORT" : 0,

    # Nickname that the bot on the IRC server will have
    "IRCBOT_NAME" : "b-test",

    # Full name that the bot has on IRC. This info is displayed when the bot is
    # whois'ed
    "IRCBOT_LONG_NAME" : "Bot qui relaie les messages slack<->irc<->mattermost",

    #auth token of the bot on slack
    #(be sure to invite the bot to any chan you with to connect with irc)
    "SLACKBOT_TOKEN" : "",

    #time between two queries to retrieve messages on slack
    "SLACKBOT_REFRESH_TIME" : 1, #in seconds

    #IP adress to bind the webserver needed by mattermost
    "MMBOT_BINDING_IP" : "",

    #port to bind the webserver needed by mattermost
    "MMBOT_BINDING_PORT" : 0,

    #secret URL to which we should send our requests to MM
    "MMBOT_INHOOK_URL" : "",

    #tokens that MM should send you with every get_request
    #there has to be one outgoing hook for each channel on MM that you wish to twins
    #this should be a list containing one or more tokens, serialized with json
    "MMBOT_OUTHOOK_TOKEN" : '["", ""]',

    #slack icon used to imperson external posters
    "SLACK_ICON_EMOJI" : "cubimal-chick",

    #activates or disables sending a message when the bot connects (True or False)
    "WELCOME_MESSAGES" : False
}

env = os.environ # retrieve environement variables
for key in env:
    if key in cfg.keys():    # if a config option was defined
        cfg[key] = env[key]

# load MMBOT_OUTHOOK_TOKEN from json
cfg["MMBOT_OUTHOOK_TOKEN"] = json.loads(cfg["MMBOT_OUTHOOK_TOKEN"])
