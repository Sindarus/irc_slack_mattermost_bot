#!/usr/bin/env python2
# -*- coding: utf8 -*-

from copy import *

from chan import *

class TwinningTable:
    """singleton class that stores what chans to link with eachother"""

    def __init__(self, table):
        self.table = table

        #checking twinning table integrity
        assert isinstance(table, list), "TWINNINGS config option should be a list"
        for cur_twinning in table:
            assert isinstance(cur_twinning, list), "each item of TWINNINGS should be a list"
            for cur_chan in cur_twinning:
                assert isinstance(cur_chan, Chan), "each item of a twinning should be a chan object"
                assert len(self.get_chan_twins(cur_chan)) > 0, "a twinning should contain at least two chans"

    def get_chan_twins(self, chan):
        """Returns a list of chans that are twins of `chan`."""

        assert isinstance(chan, Chan), "The chan argument should be a Chan object"

        for cur_twinning in self.table:
            for i, cur_chan in enumerate(cur_twinning):
                if cur_chan == chan:
                    ret = deepcopy(cur_twinning)
                    ret.pop(i)
                    return ret

        return []   # if we couldn't find the chan in the twinning table

    def get_twinning_index(self, chan):
        """Returns the index of the twinning that contains `chan` or -1 if the chan
        is not in the twinning table"""
        for i in range(len(self.table)):
            for cur_chan in self.table[i]:
                 if cur_chan == chan:
                     return i
        return -1

    def get_all_chans(self):
        """returns the list of all the chans present in this twinning table. if a chan
        appears in several twinnings, it is only listed once"""
        chan_list = []
        for cur_twinning in self.table:
            for cur_chan in cur_twinning:
                if not cur_chan in chan_list:
                    chan_list.push(cur_chan)
        return chan_list

    def get_chan_by_server(self, server):
        """returns the list of the chans on the "server" chat server"""
        chan_list = []
        for cur_twinning in self.table:
            for cur_chan in cur_twinning:
                if cur_chan.chat_server == server:
                    chan_list.push(cur_chan)

    def __repr__(self):
        return self.table.__repr__()
