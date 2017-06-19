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

import os, sys
from elivepatch_client.client.checkers import CVE
from elivepatch_client.client.checkers import Kernel
from elivepatch_client.client.restful import ManaGer
from elivepatch_client.client.version import VERSION


if sys.hexversion >= 0x30200f0:
    ALL_KEYWORD = b'ALL'
else:
    ALL_KEYWORD = 'ALL'


class Main(object):
    """Performs the actions the user selected.
    """

    def __init__(self, argparser):
        config = argparser.get_arg()
        self.dispatch(config)
        # print(config)
        # print(Kernel().get_version())
        # self.url = config.url
        # self.send_config()


    def dispatch(self, config):
        print(str(config))
        if config.cve:
            print('working on cve')
            Kernel()
        elif config.patch:
            print('working with patch')
            Kernel().get_version()
        elif config.version:
            print('elivepatch version: '+str(VERSION))
        else:
            print('--help for help\n\
you need at list --patch or --cve')



    def __call__(self):
        pass

    def send_config(self):
        server = ManaGer(self.url)
        pass
