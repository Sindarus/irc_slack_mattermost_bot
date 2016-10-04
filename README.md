# slack_irc_bot_python
Bot that twins IRC channels with Slack channels and with Mattermost
This was developped for use inside ENSIIE Strasbourg and it may lack flexibility. However, feel free to fork it.

## How to run it
* install python 2.7
* install `irclib` and `ircbot` python modules with `sudo apt-get install python-irclib`
* install the pip module manager
* install the slack client module with `sudo pip install slackclient` (doc here [http://python-slackclient.readthedocs.io/en/latest/?badge=latest])
* install web.py with `pip install web.py`

## Global functionning
This programm is about a bot, but it actually has 3 inside : one per plateform to deal with. When the three bots work together, the programm acts like a unique bot that has as many faces as there are plateforms.
There is one singleton class (one bot) per plateform to deal with : IrcBot for irc, mmbot for mattermost and SlackBot for slack. Actually, mmbot is not a class but a module. Functions defined in `mm_bot`, can be called like `mm_bot` was an object by importing the module with `import mm_bot`. Example : `mm_bot.start()`.
Each bot has a `start()` method, and each bot runs in a thread that is separated from the main thread. When one of the three bots receives a message, it calls `handle_msg()` in `central_unit.py`. This function is in charge of routing the messages to the right destination channels. Each bot has a `post_msg()` method that `handle_msg()` calls to send messages on a specific channel of said plateform.