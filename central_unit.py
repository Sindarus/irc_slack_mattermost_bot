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
from mm_bot import *
from config import cfg as c

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
    twins = c["TWINNINGS"].get_chan_twins(msg.chan_orig)

    for cur_chan in twins:
        post_msg_on_chan(msg, cur_chan)

    do_commands(msg)

def post_msg_on_chan(msg, chan):
    """posts msg on chan"""
    if chan.chat_type == "IRC":
        my_ircbot.post_msg(chan.chan_name, msg)
    elif chan.chat_type == "Slack":
        my_slackbot.post_msg(chan.chan_name, msg)
    elif chan.chat_type == "MM":
        my_mmbot.post_msg(chan.chan_name, msg)
    else:
        v.log(1, "While handling a message : Unknown chat type")

def broadcast(msg, twinning_index = -1):
    """Sends msg to all chan in the twinnning that has twinning_index as index,
    if twinning_index is left unset (it is optional), the msg is sent to ALL chans that
    appear in the twinning table"""
    if twinning_index == -1:
	for chan in twinnings.get_all_chans():
            post_msg_on_chan(msg, chan)
    else:
        for chan in twinnings.table[twinning_index]:
            post_msg_on_chan(msg, chan)

def do_commands(in_msg):
    """Checks if there are commands intended for the twinning bot to execute. If there are
    respond in the source chan and all its twins"""
    if in_msg.msg.find("!twinning_bot") == 0: # if msg starts with !twinning_bot
        if(in_msg.msg == "!twinning_bot help"):
            text = "Available commands : help, isup, current_twinnings."
        elif(in_msg.msg == "!twinning_bot isup"):
            text = "Twinning bot is UP."
        elif(in_msg.msg == "!twinning_bot current_twinnings"):
            text = "Current twinnings are : " + str(twinnings.table)
        else:
            text = "Unknown command. See !twinning_bot help."

        msg = Message(in_msg.chan_orig, "Twinning bot", text)
        twinning_index = twinnings.get_twinning_index(in_msg.chan_orig)
        if(twinning_index != -1): # if chan_orig was found in the twinning table
            broadcast(msg, twinning_index)
        else:
            post_msg_on_chan(msg, in_msg.chan_orig)

def start():
    """starts the whole system by retrieving config.py options, creating
    the bots and launching them in a separate thread"""

    #needed to change global variables
    global twinnings
    global my_ircbot
    global my_slackbot
    global my_mmbot

    #loading twinning table from config file
    v.log(3, "loading twinning table")
    v.log(3, c["TWINNINGS"])

    #creating bots
    v.log(3, "creating ircbot")
    my_ircbot = IrcBot()
    v.log(3, "creating slackbot")
    my_slackbot = SlackBot()
    v.log(3, "creating mmbot")
    my_mmbot = MmBot()

    #preparing threads
    #we set the flag "Deamon" on each thread. The whole programm quits when
    #there is no non-deamon thread running; in our case : when the original
    #thread terminates.
    irc_thread = threading.Thread(target=my_ircbot.start, name="irc thread")
    irc_thread.setDaemon(True)
    slackbot_thread = threading.Thread(target=my_slackbot.start, name="slackbot thread")
    slackbot_thread.setDaemon(True)
    mmbot_thread = threading.Thread(target=my_mmbot.start, name="mmbot thread")
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
        try:
            s = raw_input()
        except Exception, e:
            time.sleep(60)

    print("======= QUITTING ! =======")
