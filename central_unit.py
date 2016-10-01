#!/usr/bin/env python2
# -*- coding: utf8 -*-

import threading
import time

import verbose as v
from twinning_table import *
from message import *
from chan import *
from irc_bot import *
from slack_bot import *
import mm_bot
from config import cfg as c
from config import TWINNINGS

#I know using global variable is considered to be a bad habit,
#but in this case, they are useful and simple enough to not make the program dirty.
#Anyways, this module can be considered as an object, whose global variables here
#can be accessed with central_unit.variable

def handle_msg(msg):
    """This is the 'centralunit' : This function is called by the bots monitoring
    IRC, Slack or MM when they receive a message. This function then looks for
    the chans that the message need to be sent on (chans that are twins of the
    chan from which the message comes), and then calls the right bots
    so that the messages are sent on every chan twins"""

    assert isinstance(msg, Message), "msg has to be a Message object, was a " + type(Message).__name__

    v.log(4, ["handling msg : ", msg.__repr__()])
    twins = twinnings.get_chan_twins(msg.chan_orig)

    for cur_chan in twins:
        if cur_chan.chat_type == "IRC":
            my_ircbot.post_msg(cur_chan.chan_name, msg)
        elif cur_chan.chat_type == "Slack":
            my_slackbot.post_msg(cur_chan.chan_name, msg)
        elif cur_chan.chat_type == "MM":
            mm_bot.post_msg(cur_chan.chan_name, msg)
        else:
            v.log(1, "While handling a message : Unknown chat type")

def start():
    """starts the whole system by retrieving config.py options, creating
    the bots and launching them in a separate thread"""

    #needed to change global variables
    global twinnings
    global my_ircbot
    global my_slackbot

    #loading twinning table from config file
    v.log(3, "loading twinning table")
    twinnings = TwinningTable(TWINNINGS)
    v.log(3, twinnings)

    #creating bots
    v.log(3, "creating ircbot")
    my_ircbot = IrcBot()
    v.log(3, "creating slackbot")
    my_slackbot = SlackBot()


    #preparing threads
    #we set the flag "Deamon" on each thread. The whole programm quits when
    #there is no non-deamon thread running; in our case : when the original
    #thread terminates.
    irc_thread = threading.Thread(target=my_ircbot.start, name="irc thread")
    irc_thread.setDaemon(True)
    slackbot_thread = threading.Thread(target=my_slackbot.start, name="slackbot thread")
    slackbot_thread.setDaemon(True)
    mmbot_thread = threading.Thread(target=mm_bot.start, name="mmbot thread")
    mmbot_thread.setDaemon(True)

    #running bots
    v.log(3, "starting ircbot in a thread")
    irc_thread.start()
    v.log(3, "starting slackbot in a thread")
    slackbot_thread.start()
    v.log(3, "starting mmbot in a thread")
    mmbot_thread.start()

    s = ""
    while(s != "quit" and s != "exit"):
        print("======= Enter 'quit' or 'exit' anytime to quit the programm =======")
        s = raw_input()

    print("======= QUITTING ! =======")
