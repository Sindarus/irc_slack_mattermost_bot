#!/usr/bin/env python2
# -*- coding: utf8 -*-

from chan import *

class Message:
    def __init__(self, chan_orig, author, msg):
        assert isinstance(chan_orig, Chan), "chan_orig has to be a Chan object"
        assert isinstance(author, str), "author has to be a string"
        if not isinstance(msg, str):
            print("Msg has to be a string. msg : " + msg + " type : " + type(msg).__name__)

        self.chan_orig = chan_orig
        self.author = author
        self.msg = msg

    def __repr__(self):
        ret = "(" + self.chan_orig.chat_type + " " + self.chan_orig.chan_name + ")"
        ret += " <" + self.author + "> " + self.msg
        return ret
