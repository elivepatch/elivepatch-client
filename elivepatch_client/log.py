# Copyright 2003-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

"""Logging related code (taken from Gentoo Catalyst)
This largely exposes the same interface as the logging module except we add
another level "notice" between warning & info, and all output goes through
the "elivepatch" logger.
"""

from __future__ import print_function

import logging
import logging.handlers
import os
import sys
import time


class elivepatchLogger(logging.Logger):
        """Override the _log member to autosplit on new lines"""

        def _log(self, level, msg, args, **kwargs):
                """If given a multiline message, split it"""
                # We have to interpolate it first in case they spread things out
                # over multiple lines like: Bad Thing:\n%s\nGoodbye!
                try:
                    msg %= args
                    for line in msg.splitlines():
                            super(elivepatchLogger, self)._log(level, line, (), **kwargs)
                except:
                    print("msg")
                    print(msg)
                    print("args")
                    print(args)


# The logger that all output should go through.
# This is ugly because we want to not perturb the logging module state.
_klass = logging.getLoggerClass()
logging.setLoggerClass(elivepatchLogger)
logger = logging.getLogger('elivepatch')
logging.setLoggerClass(_klass)
del _klass


# Set the notice level between warning and info.
NOTICE = (logging.WARNING + logging.INFO) // 2
logging.addLevelName(NOTICE, 'NOTICE')


# The API we expose to consumers.
def notice(msg, *args, **kwargs):
        """Log a notice message"""
        logger.log(NOTICE, msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
        """Log a critical message and then exit"""
        status = kwargs.pop('status', 1)
        logger.critical(msg, *args, **kwargs)
        sys.exit(status)

error = logger.error
warning = logger.warning
info = logger.info
debug = logger.debug


class elivepatchFormatter(logging.Formatter):
        """Mark bad messages with colors automatically"""

        _COLORS = {
                'CRITICAL':     '\033[1;35m',
                'ERROR':        '\033[1;31m',
                'WARNING':      '\033[1;33m',
                'DEBUG':        '\033[1;34m',
        }
        _NORMAL = '\033[0m'

        @staticmethod
        def detect_color():
                """Figure out whether the runtime env wants color"""
                if 'NOCOLOR' is os.environ:
                        return False
                return os.isatty(sys.stdout.fileno())

        def __init__(self, *args, **kwargs):
                """Initialize"""
                color = kwargs.pop('color', None)
                if color is None:
                        color = self.detect_color()
                if not color:
                        self._COLORS = {}

                super(elivepatchFormatter, self).__init__(*args, **kwargs)

        def format(self, record, **kwargs):
                """Format the |record| with our color settings"""
                msg = super(elivepatchFormatter, self).format(record, **kwargs)
                color = self._COLORS.get(record.levelname)
                if color:
                        return color + msg + self._NORMAL
                else:
                        return msg


# We define |debug| in global scope so people can call log.debug(), but it
# makes the linter complain when we have a |debug| keyword.  Since we don't
# use that func in here, it's not a problem, so silence the warning.
# pylint: disable=redefined-outer-name
def setup_logging(level, output=None, debug=False, color=None):
        """Initialize the logging module using the |level| level"""
        # The incoming level will be things like "info", but setLevel wants
        # the numeric constant.  Convert it here.
        try:
            level = logging.getLevelName(level.upper())

            # The good stuff.
            fmt = '%(asctime)s: %(levelname)-8s: '
            if debug:
                    fmt += '%(filename)s:%(funcName)s: '
            fmt += '%(message)s'

            # Figure out where to send the log output.
            if output is None:
                    handler = logging.StreamHandler(stream=sys.stdout)
            else:
                    handler = logging.FileHandler(output)

            # Use a date format that is readable by humans & machines.
            # Think e-mail/RFC 2822: 05 Oct 2013 18:58:50 EST
            tzname = time.strftime('%Z', time.localtime())
            datefmt = '%d %b %Y %H:%M:%S ' + tzname
            formatter = elivepatchFormatter(fmt, datefmt, color=color)
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            logger.setLevel(level)
        except:
            pass
