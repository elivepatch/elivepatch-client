#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
from elivepatch_client.client.version import VERSION


class ArgsParser():
    def __init__(self):
        @click.command()
        @click.option('-c','--cve', default=False, help='Check for secutiry problems in the kernel.', is_flag=True)
        @click.option('-p','--patch', help='patch to convert.')
        @click.option('-k','--kernel', help='set kernel folder manually.',type=click.Path())
        @click.option('-d','--debug', help='set the debug option.', is_flag=True)
        @click.option('-v', '--verbose', count=True, help='set the verbose option.')
        @click.version_option(version=VERSION)

        def saas(cve, patch, kernel, debug, verbose):
            print("cve", cve)
            print("patch", patch)
            print("kernel",kernel)
            print("debug", debug)

            pass

        saas()

