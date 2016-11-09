#!/usr/bin/env python2
# -*- coding: utf8 -*-

class ChatServer:
    """Chat server such as AAA.slack.com or BBB.slack.com or irc.freenode.net or slack.***.eu (mattermost)"""

    def __init__(self, chat_type, display_name, server_adress=None, server_port=None, slack_bot_token=None, outhook_tokens=None, inhook_url=None):
        self.type = chat_type
        self.display_name = display_name
        self.bot = None

        if chat_type == "IRC":
            if server_adress == None or server_port == None:
                v.log(1, "In ChatServer.__init__ : you need to specify a server adress and port for an IRC server")
                exit(1)
            self.server_adress = server_adress
            self.server_port = server_port
        elif chat_type == "Slack":
            if slack_bot_token == None:
                v.log(1, "In ChatServer.__init__ : you need to specify slack_bot_token for a slack server")
                exit(1)
            self.slack_bot_token = slack_bot_token
        elif chat_type == "MM":
            if outhook_tokens == None:
                v.log(1, "In ChatServer.__init__ : you need to specify outhook_tokens for a MM server")
                exit(1)
            if inhook_url == None:
                v.log(1, "In ChatServer.__init__ : you need to specify inhook_url for a MM server")
                exit(1)
            self.outhook_tokens = outhook_tokens
            self.inhook_url = inhook_url
        else:
            v.log(1, "In ChatServer.__init__ : Unknown chat type.")
            exit(1)

    def __repr__(self):
        return self.type + " server <" + self.display_name + "> #" + hex(id(self)).__repr__()
