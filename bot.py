#!/usr/bin/env python2
# -*- coding: utf8 -*-

import threading
import time

import irclib
import ircbot

from slackclient import SlackClient

class IrcBot(ircbot.SingleServerIRCBot):
    def __init__(self):
        """
        Constructeur qui pourrait prendre des paramètres dans un "vrai" programme.
        """
        print("connecting to irc")
        ircbot.SingleServerIRCBot.__init__(self, [("irc.iiens.net", 6667)],
                                           "relai-slack", "Bot qui relaie les message postés sur slack")
        print("connected to irc")

    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        Notez qu'on ne peut rejoindre les canaux auparavant.
        """
        print("joining chan")
        serv.join("#test-ircbot")
        print("joined chan")
        serv.privmsg("#test-ircbot", "Bonjour tout le monde, je suis un bot qui retransmet ici les messages postés sur slack, et qui retransmet sur slack les messages postés ici.")

    def on_pubmsg(self, serv, ev):
        """
        Méthode appelée à la réception d'un message sur irc.
        """

        # Il n'est pas indispensable de passer par des variables
        # Ici elles permettent de clarifier le tout.
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0].lower()

        print("( IRC ) " + auteur + " : " + message)

        #sending msg to slack
        client.api_call( "chat.postMessage",
                   channel="#bot-testing",
                   text=message,
                   username=auteur,
                   icon_emoji=':robot_face:'
        )

        #this used to send a msg on the irc channel
        #serv.privmsg(canal, "Bonjour " + auteur)

def start_irc_bot():
    IrcBot().start()

# PROGRAM STARTS HERE ========================================================
print("Initiating slackclient")
token = "xoxb-78808818897-Hw70mg5wQuADBJUJJvxO8CFy"
client = SlackClient(token)
print("Slackclient initiated")

client.api_call( "chat.postMessage",
                   channel="#bot-testing",
                   text="Bonjour tout le monde, je suis un bot qui retransmet ici les messages postés sur irc, et qui retransmet sur irc les messages postés ici.",
                   username="relai-irc",
                   icon_emoji=':robot_face:'
        )

print("starting irc bot in a thread")
threading.Thread(target=start_irc_bot).start()

print("Launching main loop for slack")
if client.rtm_connect():
    print("Successfully started real time messaging system for slack")
    while True:
        print("reading slack messages?")
        last_read = client.rtm_read()
        if last_read:
            try:
                msg = last_read[0]['text']
                #reply to channel message was found in.
                channel = last_read[0]['channel']
                
                print("(SLACK) " + "?????" + " : " + msg)
                print("we still need to send it to irc")
            except:
                print("No slack messages...");
                pass
        else :
            print("last_read evaluates to false...")
            print(last_read)
        time.sleep(2)
else:
    print("There was a problem starting the real time messaging system for slack")








