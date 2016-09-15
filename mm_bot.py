#!/usr/bin/env python2
# -*- coding: utf8 -*-

import web
import urllib2  # to send get requests

import config
import central_unit

urls = (
    '/handle_msg', 'hello'
)
app = web.application(urls, globals())

class hello:
    def POST(self):
        print("MMBOT: received a post request")
        input = web.input()
        if(input.token != c.MMBOT_OUTHOOK_TOKEN):
            print("WARNING: MMBOT received a post request but the token was wrong. Ignoring request.")
            return

        try:
            print("MMBOT: transfering message to central_unit")
            central_unit.handle_msg(Message(
                chan_orig=Chan("MM", input.channel_name),
                author=input.user_name,
                msg=input.text)
            )
        except Exception, e:
            print("MMBOT: could not process the message because : " + e.__repr__())
            return

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
