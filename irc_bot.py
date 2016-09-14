#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot

import config as c
import central_unit

from message import *
from chan import *

class IrcBot(ircbot.SingleServerIRCBot):
    """
    Bot that runs in a separate thread, that deals with irc interaction
    """

    def __init__(self):
        print("IRCBOT: Connecting to irc")
        self.connected = False
        ircbot.SingleServerIRCBot.__init__(
            self,
            [(c.IRC_SERVER, c.IRC_PORT)],
            c.IRCBOT_NAME,
            c.IRCBOT_LONG_NAME
        )

    def join_to_chans(self):
        """Make ircbot join all the channels that need to be monitored"""
        print("IRCBOT: joining chans")
        for cur_twinning in central_unit.twinnings.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_type == "IRC":
                    print("IRCBOT: joining " + cur_chan.chan_name)
                    self.serv.join(cur_chan.chan_name)

    def on_welcome(self, serv, ev):
        """
        Method that is called once we're connected and identified.
        Note that you can join channel before that.
        """

        print("IRCBOT: connected to irc")
        self.connected = True
        self.serv = serv

        self.join_to_chans()

        if c.WELCOME_MESSAGES:
            self.send_welcome_msg()

    def on_pubmsg(self, serv, ev):
        """
        Method called when a message is received on IRC. Transmits the message
        to the central unit, as a Message object
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
        """
        Sends a welcome message on every channel that is twinned with another
        one. The message tells with what other channels the said channel is
        twinned with.
        """

        print("IRCBOT: sending welcome message")
        for cur_twinning in central_unit.twinnings.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_type == "IRC":
                    self.serv.privmsg(
                        cur_chan.chan_name,
                        "(Init) Twinning this chan with : " + central_unit.twinnings.get_chan_twins(cur_chan).__repr__()
                    )

    def post_msg(self, chan_name, msg):
        """Posts a message on the channel `chan_name` on IRC. This function
        handles formatting the message to make it look like the author of the
        message posted it."""

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
