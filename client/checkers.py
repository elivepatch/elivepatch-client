#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import gzip
import uuid

import os
import os.path
import re
from git import Repo

from elivepatch_client.client import restful


def id_generate_uuid():
    generated_uuid = str(uuid.uuid4())
    return generated_uuid


class Kernel(object):
    """
    Class for manage the kernels files
    """

    def __init__(self, restserver_url, session_uuid=None):
        self.config_fullpath = ''
        self.patch_fullpath = ''
        self.restserver_url = restserver_url
        self.kernel_version = None
        if session_uuid:
            self.session_uuid = session_uuid
        else:
            self.session_uuid = id_generate_uuid()
        print('This session uuid: ' + str(self.session_uuid))
        self.rest_manager = restful.ManaGer(self.restserver_url, self.kernel_version, self.session_uuid)

    def set_config(self, config_fullpath):
        self.config_fullpath = config_fullpath

    def set_patch(self, patch_fullpath):
        self.patch_fullpath = patch_fullpath

    def send_files(self):
        """
        Send config and patch files

        :return: void
        """
        path, file = (os.path.split(self.config_fullpath))
        f_action = FileAction(path, file)
        # check the configuration file
        if re.findall("[.]gz\Z", self.config_fullpath):
            print('gz extension')
            path, file = f_action.ungz()
            # if the file is .gz the configuration path is the tmp folder uncompressed config file
            self.config_fullpath = os.path.join(path, file)

        # Get kernel version from the configuration file header
        self.kernel_version = f_action.config_kernel_version(self.config_fullpath)
        self.rest_manager.set_kernel_version(self.kernel_version)
        print('debug: kernel version = ' + self.rest_manager.get_kernel_version())

        path, patch_filename = (os.path.split(self.patch_fullpath))
        send_api = '/elivepatch/api/v1.0/get_files'

        # send uncompressed config and patch files
        self.rest_manager.send_file(self.config_fullpath, self.patch_fullpath, file, patch_filename, send_api)

    def build_livepatch(self):
        self.rest_manager.build_livepatch()

    def get_livepatch(self):
        self.rest_manager.get_livepatch()


class CVE(object):

    def __init__(self):
        self.git_url = "https://github.com/nluedtke/linux_kernel_cves"
        self.repo_dir = "/tmp/kernel_cve/"
        pass

    def download(self):
        Repo.clone_from(self.git_url, self.repo_dir)

    def set_repo(self, git_url, repo_dir):
        self.git_url = git_url
        self.repo_dir = repo_dir


class FileAction(object):

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        pass

    def ungz(self):
        path_to_store = None
        path_gz_file = os.path.join(self.path, self.filename)
        temporary_path_uncompressed_file = os.path.join('/tmp', self.filename)
        print('path_gz_file: '+ path_gz_file + ' temporary_path_uncompressed_file: ' +
              temporary_path_uncompressed_file)
        if not os.path.isdir(path_gz_file):
            with gzip.open(path_gz_file, 'rb') as in_file:
                s = in_file.read()
            # Store uncompressed file
            path_to_store = temporary_path_uncompressed_file[:-3]  # remove the filename extension
            with open(path_to_store, 'wb') as f:
                f.write(s)
            print('working')
            path, uncompressed_file = (os.path.split(path_to_store))
        return path, uncompressed_file

    def config_kernel_version(self, uncompressed_config_file):
        with open(uncompressed_config_file) as f:
            i = 0
            while i < 2:
                f.readline()
                if i == 1:
                    kernel_line = f.readline()
                i += 1
        kernel_version_raw = (kernel_line.split(' ')[2])
        kernel_version = kernel_version_raw.split(('-'))[0]
        return kernel_version

