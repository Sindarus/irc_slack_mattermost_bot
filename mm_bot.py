#!/usr/bin/env python2
# -*- coding: utf8 -*-

import web
import urllib2  # to send get requests

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
        print("MMBOT: received a post request")
        input = web.input()
        if(input.token not in c.MMBOT_OUTHOOK_TOKEN):
            print("WARNING: MMBOT received a post request but the token was wrong. Ignoring request.")
	    print("token was : " + input.token + " expecting : " + c.MMBOT_OUTHOOK_TOKEN.__repr__())
            return

        try:
            channel_name = input.channel_name
            user_name = input.user_name
            text = input.text
        except Exception, e:
            print("MMBOT: receied post request did not contain all needed data. Got exception : " + e.__repr__())
            return

        print("MMBOT: transfering message to central_unit")
        central_unit.handle_msg(Message(
            chan_orig=Chan("MM", channel_name.encode("utf-8")),
            author=user_name.encode("utf-8"),
            msg=text.encode("utf-8"))
        )

def start():
    print("MMBOT: launching")
    web.httpserver.runsimple(app.wsgifunc(), (c.MMBOT_BINDING_IP, c.MMBOT_BINDING_PORT))

def post_msg(chan_name, msg):
    assert isinstance(chan_name, str), "Chan_name should be a string, was a " + type(chan_name).__name__
    assert isinstance(msg, Message), "msg should be a Message, was a " + type(msg).__name__

    # preparing request to send to MM API
    author = msg.author #this is needed for the string formatting to work
    msg = msg.msg
    request = 'payload={"channel": "%(chan_name)s", "username" : "%(author)s", "text": "%(msg)s"}' % locals()

    print("MMBOT: posting to MM")
    res = urllib2.urlopen(c.MMBOT_INHOOK_URL, request)
    if(res.getcode() != 200):
        print "WARNING : Tried to post a msg on MM but MM returned response code != 200"
