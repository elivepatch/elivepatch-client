#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later


import argparse
try:
    import ConfigParser
except:
    import configparser as ConfigParser

class ArgsParser(object):

    def __init__(self):
        conf_parser = argparse.ArgumentParser(
            # Turn off help, so we print all options in response to -h
            add_help=False
        )
        conf_parser.add_argument("-c", "--conf_file",
                                 help="Specify config file", metavar="FILE")
        args, remaining_argv = conf_parser.parse_known_args()
        defaults = {
            "config" : "/proc/config.gz",
        }
        if args.conf_file:
            config = ConfigParser.SafeConfigParser()
            config.read([args.conf_file])
            defaults = dict(config.items("Defaults"))

        # Don't surpress add_help here so it will handle -h
        parser = argparse.ArgumentParser(
            # Inherit options from config_parser
            parents=[conf_parser],
            # print script description with -h/--help
            description=__doc__,
            # Don't mess with format of description
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.set_defaults(**defaults)
        parser.add_argument("-e","--cve", action='store_true', help="Check for secutiry problems in the kernel.")
        parser.add_argument("-p","--patch", help="patch to convert.")
        parser.add_argument("-k","--config", help="set kernel config file manually.")
        parser.add_argument("-u","--url", help="set elivepatch server url.")
        parser.add_argument("-d","--debug", action='store_true', help="set the debug option.")
        parser.add_argument("-v","--version", action='store_true', help="show the version.")
        self.args = parser.parse_args(remaining_argv)

    def get_arg(self):
        return self.args

