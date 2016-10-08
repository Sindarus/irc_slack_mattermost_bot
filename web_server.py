#!/usr/bin/env python2
# -*- coding: utf8 -*-

import web

import central_unit
from config import cfg as c

urls = (
    '/test', 'TestAction'
    '/handle_msg', 'HandleMsgAction',
)
app = web.application(urls, globals())

def start():
    """Starts the webserver"""
    web.httpserver.runsimple(app.wsgifunc(), (c["MMBOT_BINDING_IP"], c["MMBOT_BINDING_PORT"]))

class TestAction:
    """Class associated with the /test URL"""

    def GET(self):
        """Method called when there is a GET request on /test"""
        return "This is a test page to see if the webserver is reachable."

class HandleMsgAction:
    """Class associated with the /handle_msg URL"""

    def POST(self):
        """Method called when there is a POST request on handle_msg"""
        v.log(3, "WEBSERVER: received a post request")
        input = web.input()
        if input.token not in c["MMBOT_OUTHOOK_TOKEN"]:
            v.log(1, "WEBSERVER received a post request but the token was wrong. Ignoring request.")
            v.log(1, "token was : " + input.token + " expecting : " + c["MMBOT_OUTHOOK_TOKEN"].__repr__())
            return

        try:
            channel_name = input.channel_name
            user_name = input.user_name
            text = input.text
        except Exception, e:
            v.log(1, "WEBSERVER: received post request did not contain all needed data. Got exception : " + e.__repr__())
            return

        v.log(3, "WEBSERVER: transfering message to mm_bot")
        mm_bot.receive_msg(Message(
            chan_orig=Chan("MM", channel_name.encode("utf-8")),
            author=user_name.encode("utf-8"),
            msg=text.encode("utf-8"))
        )
