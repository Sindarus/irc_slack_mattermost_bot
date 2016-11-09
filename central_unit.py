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
import config as c

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
    twins = c.TWINNINGS.get_chan_twins(msg.chan_orig)

    for cur_chan in twins:
        post_msg_on_chan(msg, cur_chan)

    do_commands(msg)

def post_msg_on_chan(msg, chan):
    """posts msg on chan"""
    chan.chat_server.bot.post_msg(chan, msg)

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

    #loading twinning table from config file
    v.log(3, "loading servers")
    v.log(3, c.SERVERS.__repr__())
    v.log(3, "loading twinning table")
    v.log(3, c.TWINNINGS.__repr__())


    #creating bots
    for server in c.SERVERS:
        if server.type == "IRC":
            v.log(3, ["creating ircbot for server ", server])
            server.bot = IrcBot(server)
        elif server.type == "MM":
            v.log(3, ["creating mmbot for server ", server])
            server.bot = MmBot(server)
        elif server.type == "Slack":
            v.log(3, ["creating slackbot for server ", server])
            server.bot = SlackBot(server)

    #preparing threads
    #we set the flag "Deamon" on each thread. The whole programm quits when
    #there is no non-deamon thread running; in our case : when the original
    #thread terminates.
    threads = []
    for server in c.SERVERS:
        cur_thread = threading.Thread(target=server.bot.start, name=server.display_name+" thread")
        cur_thread.setDaemon(True)
        threads.append(cur_thread)

    #running bots
    v.log(3, "starting all bots in separate threads")
    for thread in threads:
        thread.start()

    #interface
    s = ""
    while(s != "quit" and s != "exit"):
        print("======= Enter 'quit' or 'exit' anytime to quit the programm =======")
        try:
            s = raw_input()
        except Exception, e:
            time.sleep(60)

    print("======= QUITTING ! =======")
