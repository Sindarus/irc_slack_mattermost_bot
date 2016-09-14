#!/usr/bin/env python2
# -*- coding: utf8 -*-

from copy import *

from chan import *

class TwinningTable:
    #singleton class that stores what chans to link with eachother

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
        #returns a list of chans that are twins of `chan`
        assert isinstance(chan, Chan), "The chan argument should be a Chan object"

        for cur_twinning in self.table:
            for i, cur_chan in enumerate(cur_twinning):
                if cur_chan == chan:
                    ret = deepcopy(cur_twinning)
                    ret.pop(i)
                    return ret
        raise Exception("This chan has no twins !")

    def __repr__(self):
        return self.table.__repr__()
