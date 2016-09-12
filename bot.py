#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot

class BotBonjour(ircbot.SingleServerIRCBot):
    def __init__(self):
        """
        Constructeur qui pourrait prendre des paramètres dans un "vrai" programme.
        """
        print("connecting")
        ircbot.SingleServerIRCBot.__init__(self, [("irc.iiens.net", 6667)],
                                           "Bonjour", "Bot qui dit bonjour")
        print("connected")

    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        Notez qu'on ne peut rejoindre les canaux auparavant.
        """
        print("joining chan")
        serv.join("#test-ircbot")
        print("joined chan")
        serv.privmsg("#test-ircbot", "Bonjour tout le monde :)")

    def on_pubmsg(self, serv, ev):
        """
        Méthode appelée à la réception d'un message, qui exclut son expéditeur s'il
        écrit une insulte.
        """

        print("someone posted a message")

        # Il n'est pas indispensable de passer par des variables
        # Ici elles permettent de clarifier le tout.
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0].lower() # Les insultes sont écrites en minuscules.

        if "bonjour" in message:
            print("sending bonjour")
            serv.privmsg(canal, "Bonjour " + auteur)
    

print("START");
BotBonjour().start()
print("STOP")
