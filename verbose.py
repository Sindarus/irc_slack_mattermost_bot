#!/usr/bin/env python2
# -*- coding: utf8 -*-

import time
from datetime import datetime
from config import cfg as c

timestamp = int(time.time())
f = open('log_' + str(timestamp), 'a')

def log(level, text):
    """Utility to display pretty logs. `text` is supposed to be either an object
    to print, or a list of object to print. The time is printed along with the
    log mesage. This function handles log levels. You can choose what log levels
    to display in the config.py file.
    Everything is sent to a log file anyways"""

    # preparing string to print
    # add time
    str_to_print = datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " : "

    # add prefix
    if level == 1:
        str_to_print += "ERROR : "
    elif level == 2:
        str_to_print += "WARNING : "
    elif level == 3:
        str_to_print += "INFO : "
    elif level == 4:
        str_to_print += "TRIVIAL : "

    # add actual content to be printed
    if not isinstance(text, list):  # if user provided an object
        try:
            str_to_print += str(text)
        except Exception, e:
            print("Tried verbosing text, but got error :")
            print(e)
            return
    else:                           # if user provided a list
        for thing in text:
            try:
                str_to_print += str(thing)
            except Exception, e:
                print("Tried verbosing list, but got error :")
                print(e)
                return

    # write to file
    try:
        f.write(str_to_print)
        f.write("\n")
    except Exception, e:
        print("Tried verbosing to file, but got error :")
        print(e)

    # print to stdout (or not)
    if not level <= c["DEBUG_LEVEL"]:
        return # log is not important enough to be printed
    else:
        print(str_to_print)
