#!/usr/bin/env python2
# -*- coding: utf8 -*-

import time
import json
import unicodedata
from slackclient import SlackClient

import config as c
import central_unit

from message import *
from chan import *

class SlackBot:
    def __init__(self):
        print("SLACKBOT: Initiating slackclient")
        self.client = SlackClient(c.SLACKBOT_TOKEN)
        print("SLACKBOT: Slackclient initiated")

        self.send_welcome_msg()

    def send_welcome_msg(self):
        print("SLACKBOT: Sending welcome msg")
        for cur_twinning in central_unit.twinnings.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_type == "Slack":
                    self.client.api_call( "chat.postMessage",
                        channel="#bot-testing",
                        text="(Init) Twinning this chan with : " + central_unit.twinnings.get_chan_twins(cur_chan).__repr__(),
                        username="relai-irc",
                        icon_emoji=':robot_face:'
                    )

    def retrieve_chan_names(self):
        print("SLACKBOT: retrieving channel names")
        self.chan_names = {}
        data = self.client.api_call("channels.list")
        for channel in data["channels"]:
            self.chan_names[channel["id"]] = "#" + channel["name"]

    def chan_name(self, id):
        """Given a slack channel id, this function returns the name of the channel"""
        try:
            ret = self.chan_names[id]
        except Exception as e:  #if chan_names[id] is unknown
            self.retrieve_chan_names() #retrieve chan names again
            #try another time before giving up
            try:
                ret = self.chan_names[id]
            except Exception as e:
                print("WARNING: could not find chan name")
                ret = id #fallback: keep id as name
        return ret

    def retrieve_user_names(self):
        print("SLACKBOT: retrieving user names")
        self.user_names = {}
        data = self.client.api_call("users.list")
        for user in data["members"]:
            self.user_names[user["id"]] = user["name"]

    def user_name(self, id):
        """Given a slack user id, this function returns the name of the user"""
        try:
            ret = self.user_names[id]
        except Exception as e:  #if user_names[id] is unknown
            self.retrieve_user_names() #retrieve chan names again
            #try another time before giving up
            try:
                ret = self.user_names[id]
            except Exception as e:
                print("WARNING: could not find chan name")
                ret = id #fallback: keep id as name
        return ret

    def start(self):
        self.retrieve_chan_names()
        self.retrieve_user_names()

        print("SLACKBOT: Launching main loop for slack")
        if self.client.rtm_connect():
            print("SLACKBOT: Successfully started real time messaging system for slack")
            while True:
                print("SLACKBOT: reading slack messages?")
                last_read = self.client.rtm_read()
                msg = ""
                if last_read:
                    try:
                        msg = last_read[0]['text']
                        #convert msg from unicode to string
                        msg = unicodedata.normalize('NFKD', msg).encode('ascii','ignore')

                        channel = last_read[0]['channel']
                        #gets the real name, not the id
                        channel = self.chan_name(channel)

                        user = last_read[0]['user']
                        #gets the real name, not the id
                        user = self.user_name(user)
                        #converts user from unicode to string
                        user = unicodedata.normalize('NFKD', user).encode('ascii','ignore')

                        if msg != "":
                            print("(SLACK " + channel + ") " + user + " : " + msg)
                            central_unit.handle_msg(Message(
                                chan_orig = Chan("Slack", channel),
                                author = user,
                                msg = msg)
                            )
                    except Exception, e:
                        print("Not a message");
                        pass
                else :
                    print("No message")

                time.sleep(2)
        else:
            print("SLACKBOT: There was a problem starting the real time messaging system for slack.")
            exit()

    def post_msg(self, chan_name, msg):
        #sending msg to slack
        self.client.api_call(
            "chat.postMessage",
            channel=chan_name,
            text=msg.msg,
            username=msg.author,
            icon_emoji=c.SLACK_ICON_EMOJI
        )
