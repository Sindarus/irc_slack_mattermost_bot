#!/usr/bin/env python2
# -*- coding: utf8 -*-

import web
import urllib2  # to send get requests
import threading
import json

import verbose as v
import config as c
import central_unit
from message import *
import web_server

class MmBot:
    def __init__(self):
        pass

    def start(self):
        """Start the bot so that it begins listening to incoming messages,
        and so that it is able to send some. This method will start the
        webserver in a thread"""
        v.log(3, "MMBOT: launching webserver in a thread")
        webserver_thread = threading.Thread(target=web_server.start, name="webserver thread")
        webserver_thread.setDaemon(True)
        webserver_thread.start()
        if c.WELCOME_MESSAGES:
            self.send_welcome_msg()

    def send_welcome_msg(self):
        """Sends a welcome message on every channel that is twinned with another
        one. The message tells with what other channels the said channel is
        twinned with."""
        v.log(3, "MMBOT: Sending welcome msg")
        for cur_twinning in c.TWINNINGS.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_type == "MM":
                    msg = "(twinning bot) Twinning this chan with : " + str(c.TWINNINGS.get_chan_twins(cur_chan))
                    self.__send_request({"channel": cur_chan.chan_name, "text": msg})

    def receive_msg(self, msg):
        """Method that is called by webserver when it receives a msg from mattermost"""
        central_unit.handle_msg(msg)

    def post_msg(self, chan_name, msg):
        """Posts a message on the channel `chan_name` on mattermost. This function
        handles formatting the message to make it look like the author of the
        message posted it."""
        assert isinstance(chan_name, str), "Chan_name should be a string, was a " + type(chan_name).__name__
        assert isinstance(msg, Message), "msg should be a Message, was a " + type(msg).__name__

        # preparing request to send to MM API
        text = msg.msg
        text = text.replace("%", "%25")    # encode percent symbol
        text = text.replace(";", "%3B") # encode semicolon
        text = text.replace("&", "%26")    # encode ampersands
        text = text.replace("+", "%2B")    # encode plus symbol

        v.log(3, "MMBOT: posting to MM")
        self.__send_request({"channel": chan_name, "username": msg.author, "text": text})

    def __send_request(self, my_hash):
        """private method used to send a request to mattermost with my_hash data
        as payload"""
        payload = json.dumps(my_hash)
        request = 'payload=' + payload

        try:
            res = urllib2.urlopen(c.MMBOT_INHOOK_URL, request)
        except Exception, e:
            v.log(1, ["Tried posting to MM but got error : ", e, "\nRequest sent was : ", request])
            return

        if(res.getcode() != 200):
            v.log(2, ["WARNING : Tried to post a msg on MM but MM returned response code != 200. request sent was : ", request])
