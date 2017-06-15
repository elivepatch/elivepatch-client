#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals




################################################################################
##
## Color codes (taken from portage)
##
################################################################################

esc_seq = '\x1b['

codes = {}
codes['reset']     = esc_seq + '39;49;00m'
codes['red']       = esc_seq + '31;01m'
codes['green']     = esc_seq + '32;01m'
codes['yellow']    = esc_seq + '33;01m'
codes['turquoise'] = esc_seq + '36;01m'

OFF = 0
WARN_LEVEL = 4
INFO_LEVEL = 4
NOTE_LEVEL = 4
DEBUG_LEVEL = 4
DEBUG_VERBOSITY = 2

FAILURE = 1
SUCCEED = 0