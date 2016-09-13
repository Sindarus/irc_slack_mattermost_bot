#!/usr/bin/env python2
# -*- coding: utf8 -*-

# In this simple script, there are two global variables : my_ircbot
# and my_slackbot, that are instances of IrcBot and SlackBot.
# Each of the bot needs to be callable from any other bot, so I thought this
# would be simpler than sending each bots references to each other bot.
# Each bot runs in a separate thread.

import threading

import config as c

# PROGRAM STARTS HERE ========================================================
def start_ircbot():
    global my_ircbot        #needed to retrieve my_ircbot global variable
    my_ircbot.start()

def start_slackbot():
    global my_slackbot        #needed to retrieve my_slackbot global variable
    my_slackbot.start()

#creates global variables that will hold the instances of bots
my_ircbot = IrcBot()
my_slackbot = SlackBot()


print("starting ircbot in a thread")
threading.Thread(target=start_ircbot).start()
print("starting slackbot in a thread")
threading.Thread(target=start_slackbot).start()
