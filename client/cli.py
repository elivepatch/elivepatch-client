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
                current_kernel = Kernel(config.url, config.kernel_version)
                current_kernel.set_config(config.config)
                current_kernel.set_main_patch(cve_patch)
                current_kernel.send_files(applied_patches_list)
                current_kernel.get_livepatch()
        elif config.patch:
            patch_manager = patch.ManaGer()
            applied_patches_list = patch_manager.list(config.kernel_version)
            print(applied_patches_list)
            current_kernel = Kernel(config.url, config.kernel_version)
            current_kernel.set_config(config.config)
            current_kernel.set_main_patch(config.patch)
            current_kernel.send_files(applied_patches_list)
            current_kernel.get_livepatch()
        elif config.version:
            print('elivepatch version: '+str(VERSION))
        else:
            print('--help for help\n\
you need at list --patch or --cve')



    def __call__(self):
        pass

    def send_config(self):
        server = restful.ManaGer(self.url)
        pass
