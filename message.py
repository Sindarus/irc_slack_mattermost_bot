#!/usr/bin/env python2
# -*- coding: utf8 -*-

from chan import *

class Message:
    """
    Simple class to abstract a message that has an chan of origin, an author
    and a content (msg).
    """

    def __init__(self, chan_orig, author, msg):
        assert isinstance(chan_orig, Chan), "chan_orig has to be a Chan object"
        assert isinstance(author, str), "author has to be a string object"
        assert isinstance(msg, str), "Msg has to be a string object, was a " + type(msg).__name__

        self.chan_orig = chan_orig
        self.author = author
        self.msg = msg

    def __repr__(self):
        ret = "(" + self.chan_orig.chat_type + " " + self.chan_orig.chan_name + ")"
        ret += " <" + self.author + "> " + self.msg
        return ret
