import irclib
import ircbot

import config as c

class IrcBot(ircbot.SingleServerIRCBot):
    def __init__(self):
        print("IRCBOT : Connecting to irc")
        ircbot.SingleServerIRCBot.__init__(
            self,
            [(c.IRC_SERVER, c.PORT)],
            c.IRCBOT_NAME,
            c.IRCBOT_LONG_NAME
        )
        print("IRCBOT : connected to irc")

    def on_welcome(self, serv, ev):
        """
        Method that is called once we're connected and identified.
        Note that you can join channel before that.
        """
        self.serv = serv    #this is used to interact with the server

        print("IRCBOT : joining chan")
        self.serv.join("#test-ircbot")
        print("IRCBOT : joined chan")

        self.send_welcome_msg()

    def on_pubmsg(self, serv, ev):
        """
        Method called when a message is received on IRC
        """

        author = irclib.nm_to_n(ev.source())
        chan = ev.target()
        msg = ev.arguments()[0]

        print("( IRC ) " + author + " : " + msg)

        #sending msg to slack
        client.api_call( "chat.postMessage",
                   channel="#bot-testing",
                   text=msg,
                   username="(IRC)" + author,
                   icon_emoji=':robot_face:'
        )

    def send_welcome_msg(self):
        self.serv.privmsg("#test-ircbot", c.IRCBOT_WELCOME_MSG)
        

    def post_irc_msg(self, chan, msg, author):
        print("posting to irc")
        self.serv.privmsg(chan, "<(SLACK)" + author + "> " + msg)

