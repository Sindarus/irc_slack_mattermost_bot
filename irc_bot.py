#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot

import config as c
import central_unit

from message import *
from chan import *

from global_variables import * #needed to make the irc_bot connect
                               #to every chan needed

class IrcBot(ircbot.SingleServerIRCBot):
    def __init__(self):
        print("IRCBOT: Connecting to irc")
        self.connected = False
        ircbot.SingleServerIRCBot.__init__(
            self,
            [(c.IRC_SERVER, c.IRC_PORT)],
            c.IRCBOT_NAME,
            c.IRCBOT_LONG_NAME
        )

    def on_welcome(self, serv, ev):
        """
        Method that is called once we're connected and identified.
        Note that you can join channel before that.
        """
        print("IRCBOT: connected to irc")
        self.connected = True
        self.serv = serv

        print("IRCBOT: joining chans")
        print("lol table : ")
        print(central_unit.twinnings)
        for cur_twinning in central_unit.twinnings.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_type == "IRC":
                    print("IRCBOT: joining " + cur_chan.chan_name)
                    self.serv.join(cur_chan.chan_name)
        print("IRCBOT: joined chans")

        if c.WELCOME_MESSAGES:
            self.send_welcome_msg()

    def on_pubmsg(self, serv, ev):
        """
        Method called when a message is received on IRC
        """

        author = irclib.nm_to_n(ev.source())
        chan_name = ev.target()
        msg = ev.arguments()[0]

        print("( IRC ) " + author + " : " + msg)
        central_unit.handle_msg(Message(
            chan_orig = Chan("IRC", chan_name),
            author = author,
            msg = msg)
        )

    def send_welcome_msg(self):
        print("IRCBOT: sending welcome message")
        for cur_twinning in central_unit.twinnings.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_type == "IRC":
                    self.serv.privmsg(
                        cur_chan.chan_name,
                        "(Init) Twinning this chan with : " + central_unit.twinnings.get_chan_twins(cur_chan).__repr__()
                    )

    def post_msg(self, chan_name, msg):
        """posts `msg` to `chan_name` on IRC"""
        assert isinstance(chan_name, str), "chan_name has to be a string"
        assert isinstance(msg, Message), "msg has to be a msg"

        if not self.connected:
            print("WARNING : the ircbot was requested to post a message, but it is not connected yet !")
            return

        print("IRCBOT: posting to irc")
        self.serv.privmsg(
            chan_name,
            "<" + msg.author + "> " + msg.msg
        )
