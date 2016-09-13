import time
from slackclient import SlackClient

import config as c

def SlackBot:
    def __init__(self):
        print("SLACKBOT: Initiating slackclient")
        client = SlackClient(c.SLACK_BOT_TOKEN)
        print("SLACKBOT: Slackclient initiated")
        
        send_welcome_msg()

    def send_welcome_msg(self):
        print("SLACKBOT: Sending welcome msg")
        client.api_call( "chat.postMessage",
                   channel="#bot-testing",
                   text=c.SLACK_BOT_WELCOME_MSG,
                   username="relai-irc",
                   icon_emoji=':robot_face:'
        )

    def start():
        print("Launching main loop for slack")
        if client.rtm_connect():
            print("Successfully started real time messaging system for slack")
            while True:
                print("reading slack messages?")
                last_read = client.rtm_read()
                msg = ""
                if last_read:
                    try:
                        msg = last_read[0]['text']
                        #reply to channel message was found in.
                        channel = last_read[0]['channel']
                    except Exception, e:
                        print("Not a message");
                        pass

                    if msg != "":
                        print("(SLACK) " + "?????" + " : " + msg)
                        my_ircbot.post_irc_msg_as(msg, "?????")
                        print("message transféré")
                else :
                    print("No message")
                    
                time.sleep(2)
        else:
            print("There was a problem starting the real time messaging system for slack.")
            exit()

