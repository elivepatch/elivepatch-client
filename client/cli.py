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


if sys.hexversion >= 0x30200f0:
    ALL_KEYWORD = b'ALL'
else:
    ALL_KEYWORD = 'ALL'


class Main(object):
    """Performs the actions the user selected.
    """

    def __init__(self, argparser):
        config = argparser.get_arg()
        print(config)
        print(Kernel().get_version())
        self.url = config.url
        self.send_config()

    def __call__(self):
        pass

    def send_config(self):
        ManaGer.server_url = ""

        pass