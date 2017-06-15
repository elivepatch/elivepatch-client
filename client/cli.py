#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
# ELIVEPATCH ACTIONS
#################################################################################
# File:       cli.py
#
#             Handles elivepatch actions via the command line interface.
#
# Copyright:
#             (c) 2017 Alice Ferrazzi
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Alice Ferrazzi <alicef@gentoo.org>
#

from __future__ import unicode_literals

__version__ = "$Id: cli.py 2011-01-15 23:52 PST Brian Dolbec$"


import os, sys

if sys.hexversion >= 0x30200f0:
    ALL_KEYWORD = b'ALL'
else:
    ALL_KEYWORD = 'ALL'


class Main(object):
    """Performs the actions the user selected.
    """

    def __init__(self, config):
        self.config = config


    def __call__(self):
        pass
        #if -1 in results:
        #    sys.exit(FAILURE)
        #else:
        #    sys.exit(SUCCEED)