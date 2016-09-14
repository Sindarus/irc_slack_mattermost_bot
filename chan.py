#!/usr/bin/env python2
# -*- coding: utf8 -*-

class Chan:
    """Class to abstract a chan in a chat system.
    For example : #strasbourg on IRC
    or : #general on Slack
    In this program, a Chan is specific to a server and a chat type !!"""

    def __init__(self, chat_type, chan_name):
        assert chat_type in ["IRC", "Slack", "MM"], "Unknown chat type"
        self.chat_type = chat_type
        self.chan_name = chan_name

    def __repr__(self):
        return self.chan_name + " on " + self.chat_type

    def __eq__(self, other):
        assert isinstance(other, Chan), "Cannot compare chan with non-chan object"

        return self.chat_type == other.chat_type and self.chan_name == other.chan_name
