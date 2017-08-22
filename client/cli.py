#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import sys
import os

from elivepatch_client.client.checkers import Kernel
from elivepatch_client.client import restful
from elivepatch_client.client.version import VERSION
from elivepatch_client.client import patch
from elivepatch_client.client import security

if sys.hexversion >= 0x30200f0:
    ALL_KEYWORD = b'ALL'
else:
    ALL_KEYWORD = 'ALL'


class Main(object):
    """
    Performs the actions selected by the user
    """

    def __init__(self, argparser):
        config = argparser.get_arg()
        self.dispatch(config)

    def dispatch(self, config):
        print(str(config))
        if config.cve:
            patch_manager = patch.ManaGer()
            applied_patches_list = patch_manager.list(config.kernel_version)
            print(applied_patches_list)
            cve_repository = security.CVE()
            if not os.path.isdir("/tmp/kernel_cve"):
                print("Downloading the CVE repository...")
                cve_repository.download()
            else:
                print("CVE repository already present.")
                print("updating...")
                # TODO: update repository
            cve_patch_list = cve_repository.cve_git_id()
            for cve_id, cve_patch in cve_patch_list:
                print(cve_id, cve_patch)
                livepatch(config.url, config.kernel_version, config.config, cve_patch, applied_patches_list)
        elif config.patch:
            patch_manager = patch.ManaGer()
            applied_patches_list = patch_manager.list(config.kernel_version)
            print(applied_patches_list)
            livepatch(config.url, config.kernel_version, config.config, config.patch, applied_patches_list)

        elif config.version:
            print('elivepatch version: '+str(VERSION))
        else:
            print('--help for help\n\
you need at list --patch or --cve')


def livepatch(url, kernel_version, config, main_patch, incremental_patch_names_list):
    """
    Create, get and install the live patch

    :param url: url of the elivepatch_server
    :param kernel_version: kernel version of the system to be live patched
    :param config: configuration file of the kernel we are going to live patch (DEBUG_INFO is not needed here)
    :param main_patch: the main patch that will be converted into a live patch kernel module
    :param incremental_patch_names_list: list of patch path that are already used in the kernel
    """
    current_kernel = Kernel(url, kernel_version)
    current_kernel.set_config(config)
    current_kernel.set_main_patch(main_patch)
    current_kernel.send_files(incremental_patch_names_list)
    current_kernel.get_livepatch()