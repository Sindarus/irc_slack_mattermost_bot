#!/usr/bin/env python2
# -*- coding: utf8 -*-

import web
import urllib2  # to send get requests

import verbose as v
import json
import config as c
import central_unit
from message import *

urls = (
    '/handle_msg', 'hello',
    '/test', 'bonjour'
)
app = web.application(urls, globals())

class bonjour:
    def GET(self):
	return "This is a test page to see if the webserver is reachable."

class hello:
    def POST(self):
        v.log(3, "MMBOT: received a post request")
        input = web.input()
        if input.token not in c.MMBOT_OUTHOOK_TOKEN:
            v.log(1, "MMBOT received a post request but the token was wrong. Ignoring request.")
            v.log(1, "token was : " + input.token + " expecting : " + c.MMBOT_OUTHOOK_TOKEN.__repr__())
            return

        try:
            channel_name = input.channel_name
            user_name = input.user_name
            text = input.text
        except Exception, e:
            v.log(1, "MMBOT: received post request did not contain all needed data. Got exception : " + e.__repr__())
            return

        v.log(3, "MMBOT: transfering message to central_unit")
        central_unit.handle_msg(Message(
            chan_orig=Chan("MM", channel_name.encode("utf-8")),
            author=user_name.encode("utf-8"),
            msg=text.encode("utf-8"))
        )

def start():
    v.log(3, "MMBOT: launching")
    web.httpserver.runsimple(app.wsgifunc(), (c.MMBOT_BINDING_IP, c.MMBOT_BINDING_PORT))

def post_msg(chan_name, msg):
    assert isinstance(chan_name, str), "Chan_name should be a string, was a " + type(chan_name).__name__
    assert isinstance(msg, Message), "msg should be a Message, was a " + type(msg).__name__

    # preparing request to send to MM API
    text = msg.msg.replace(";", "☮") # replace semicolon.
                                     # semicolons cause the MM parser to crash
    text = text.replace("&", "☮")    # replace ampersands
    payload = json.dumps({"channel": chan_name, "username": msg.author, "text": text})
    request = 'payload=' + payload

    v.log(3, "MMBOT: posting to MM")
    try:
        res = urllib2.urlopen(c.MMBOT_INHOOK_URL, request)
    except Exception, e:
        v.log(1, ["Tried posting to MM but got error : ", e, "\nRequest sent was : ", request])
        return

    if(res.getcode() != 200):
        v.log(2, "WARNING : Tried to post a msg on MM but MM returned response code != 200")
