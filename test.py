#!/usr/bin/env python2
# -*- coding: utf8 -*-

from chan import *

a = Chan("IRC", "#strasbourg")
b = Chan("IRC", "#jeux")
c = Chan("IRC", "#ensiie")
d = Chan("Slack", "#general")
e = Chan("Slack", "#ares")
f = Chan("Slack", "#random")

from twinning_table import *

table = TwinningTable([[a, c, d], [b, f]])

print "twins of #strasbourg on IRC are :"
print table.get_chan_twins(a)

print "twins of #ensiie on IRC are :"
print table.get_chan_twins(c)

print "twins of #random on Slack are :"
print table.get_chan_twins(f)
