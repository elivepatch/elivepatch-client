#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import gzip
import uuid
import tempfile

import os
import os.path
import re

from elivepatch_client.client import restful


def id_generate_uuid():
    generated_uuid = str(uuid.uuid4())
    return generated_uuid


class Kernel(object):
    """
    Manage kernels files
    """
    def __init__(self, restserver_url, kernel_version, session_uuid=None):
        self.config_fullpath = ''
        self.main_patch_fullpath = ''
        self.restserver_url = restserver_url
        self.kernel_version = kernel_version
        if session_uuid:
            self.session_uuid = session_uuid
        else:
            self.session_uuid = id_generate_uuid()
        print('This session uuid: ' + str(self.session_uuid))
        self.rest_manager = restful.ManaGer(self.restserver_url, self.kernel_version, self.session_uuid)

    def set_config(self, config_fullpath):
        self.config_fullpath = config_fullpath

    def set_main_patch(self, main_patch_fullpath):
        self.main_patch_fullpath = main_patch_fullpath

    def send_files(self, incremental_patches_list):
        """
        Send config and patch files

        :return: void
        """
        f_action = FileAction(self.config_fullpath)
        temporary_config = tempfile.NamedTemporaryFile(delete=False)
        # check the configuration file
        # TODO: make it more compact
        if re.findall("[.]gz\Z", self.config_fullpath):
            print('gz extension')
            # uncompress the gzip config file
            # return configuration temporary folder
            temporary_config = f_action.decompress_gz(temporary_config)
        else:
            # read already uncompressed configuration
            with open(self.config_fullpath, 'rb') as in_file:
                config = in_file.read()
                # Store uncompressed temporary file
            temporary_config.write(config)
        # Get kernel version from the configuration file header
        # self.kernel_version = f_action.config_kernel_version(temporary_config)
        self.rest_manager.set_kernel_version(self.kernel_version)
        print('debug: kernel version = ' + self.rest_manager.get_kernel_version())

        send_api = '/elivepatch/api/v1.0/get_files'

        # send uncompressed config and patch files fullpath
        self.rest_manager.send_files(temporary_config, self.main_patch_fullpath, incremental_patches_list, send_api)

    def build_livepatch(self):
        self.rest_manager.build_livepatch()

    def get_livepatch(self):
        self.rest_manager.get_livepatch(self.main_patch_fullpath)


class FileAction(object):
    """
    Work with files
    """
    def __init__(self, full_path):
        self.full_path = full_path
        pass

    def decompress_gz(self, temporary):
        """
        Uncompress gzipped configuration
        :return: Uncompressed configuration file path
        """
        path_gz_file = self.full_path
        print('path_gz_file: '+ path_gz_file + ' temporary_path_uncompressed_file: ' +
              temporary.name)
        if not os.path.isdir(path_gz_file):
            with gzip.open(path_gz_file, 'rb') as in_file:
                uncompressed_output = in_file.read()
            # Store uncompressed file
            temporary.write(uncompressed_output)
        return temporary
