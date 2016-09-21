#!/usr/bin/env python2
# -*- coding: utf8 -*-

from datetime import datetime
import config as c

def log(level, text):
    """Utility to display pretty logs. `text` is supposed to be either an object
    to print, or a list of object to print. The time is printed along with the
    log mesage. This function handles log levels. You can choose what log levels
    to display in the config.py file"""

    if not level <= c.DEBUG_LEVEL:
        return # log is not important enough to be printed

    str_to_print = datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " : "
    if not isinstance(text, list):
        try:
            str_to_print += str(text)
        except Exception, e:
            print("Tried verbosing, but got error :")
            print(e)
            return
    else:
        for thing in text:
            try:
                str_to_print += str(thing)
            except Exception, e:
                print("Tried verbosing, but got error :")
                print(e)
                return

    print(str_to_print)
