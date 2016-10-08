FROM ubuntu:16.04
RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN apt-get -y install python-irclib
RUN pip install -U pip
RUN pip install slackclient
RUN pip install web.py
RUN echo "bonjour"
RUN git clone https://github.com/Sindarus/slack_irc_bot_python.git /home/bot/
RUN pip install -r /home/bot/requirements.txt; echo "bonjour"
CMD python -u /home/bot/main.py | tee /home/bot/log.txt

