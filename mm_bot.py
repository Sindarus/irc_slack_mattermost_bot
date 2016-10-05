#!/usr/bin/env python2
# -*- coding: utf8 -*-

import web
import urllib2  # to send get requests
import threading
import json

import verbose as v
from config import cfg as c
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
        if input.token not in c["MMBOT_OUTHOOK_TOKEN"]:
            v.log(1, "MMBOT received a post request but the token was wrong. Ignoring request.")
            v.log(1, "token was : " + input.token + " expecting : " + c["MMBOT_OUTHOOK_TOKEN"].__repr__())
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
    webserver_thread = threading.Thread(target=launch_webserver, name="webserver thread")
    webserver_thread.setDaemon(True)
    webserver_thread.start()
    if c["WELCOME_MESSAGES"]:
        send_welcome_msg()

def launch_webserver():
    web.httpserver.runsimple(app.wsgifunc(), (c["MMBOT_BINDING_IP"], c["MMBOT_BINDING_PORT"]))

def send_welcome_msg():
    v.log(3, "MMBOT: Sending welcome msg")
    for cur_twinning in central_unit.twinnings.table:
        for cur_chan in cur_twinning:
            if cur_chan.chat_type == "MM":
                msg = "(twinning bot) Twinning this chan with : " + str(central_unit.twinnings.get_chan_twins(cur_chan))
                send_request({"channel": cur_chan.chan_name, "text": msg})

def post_msg(chan_name, msg):
    assert isinstance(chan_name, str), "Chan_name should be a string, was a " + type(chan_name).__name__
    assert isinstance(msg, Message), "msg should be a Message, was a " + type(msg).__name__

    # preparing request to send to MM API
    text = msg.msg.replace(";", "☮") # replace semicolon.
                                     # semicolons cause the MM parser to crash
    text = text.replace("&", "☮")    # replace ampersands
    text = text.replace("%", "☮")    # replace percent symbol
    text = text.replace("+", "☮")    # replace plus symbol

    v.log(3, "MMBOT: posting to MM")
    send_request({"channel": chan_name, "username": msg.author, "text": text})

def send_request(my_hash):
    payload = json.dumps(my_hash)
    request = 'payload=' + payload

    try:
        res = urllib2.urlopen(c["MMBOT_INHOOK_URL"], request)
    except Exception, e:
        v.log(1, ["Tried posting to MM but got error : ", e, "\nRequest sent was : ", request])
        return

    if(res.getcode() != 200):
        v.log(2, ["WARNING : Tried to post a msg on MM but MM returned response code != 200. request sent was : ", request])
