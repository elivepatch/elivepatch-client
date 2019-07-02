#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

__version__ = '0.1'
__author__ = 'Alice Ferrazzi'
__license__ = 'GNU GPLv2+'

#===============================================================================
#
# MAIN
#
#-------------------------------------------------------------------------------
def main():
    from .argsparser import ArgsParser
    from .cli import Main
    #import pdb; pdb.set_trace()
    import os

    root = None
    try:
        root = os.environ['ROOT']
    except KeyError:
        pass

    main = Main(ArgsParser())
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupt received, exiting...')


if __name__ == "__main__":
    main()

