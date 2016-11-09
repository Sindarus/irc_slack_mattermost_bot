#!/usr/bin/env python2
# -*- coding: utf8 -*-

from chat_server import *

class Chan:
    """Class to abstract a chan in a chat system.
    For example : #strasbourg on IRC
    or : #general on Slack
    In this program, a Chan is specific to a server and a chat type !!"""

    def __init__(self, chat_server, chan_name):
        assert isinstance(chat_server, ChatServer), "chat_server should be a ChatServer object, was a " + type(chat_server).__name__
        assert isinstance(chan_name, str), "chan_name should be a str, was a " + type(chan_name).__name__
        self.chat_server = chat_server
        self.chan_name = chan_name

    def __repr__(self):
        return self.chan_name + " on " + self.chat_server.__repr__()

    def __eq__(self, other):
        assert isinstance(other, Chan), "Cannot compare chan with non-chan object"

        return self.chat_server == other.chat_server and self.chan_name == other.chan_name
