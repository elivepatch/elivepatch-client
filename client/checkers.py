#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import gzip
import shelve

import os
import os.path
import re
from git import Repo

from elivepatch_client.client import restful


class Kernel(object):

    def __init__(self, url):
        self.config = ''
        self.patch = ''
        self.url = url
        self.kernel_version = None
        self.rest_manager = restful.ManaGer(url, self.kernel_version)
        self.UserID = None

    def set_config(self, config_path):
        self.config = config_path

    def set_patch(self, patch_path):
        self.patch = patch_path

    def send_files(self):
        # check the configuration file
        path, file = (os.path.split(self.config))
        f_action = FileAction(path, file)
        if re.findall("[.]gz\Z", self.config):
            print('gz extension')
            path, file = f_action.ungz()
            # if the file is .gz the configuration path is the tmp folder uncompressed config file
            self.config = os.path.join(path,file)

        # Get kernel version from the configuration file header
        self.kernel_version = f_action.config_kernel_version(self.config)
        self.rest_manager.set_kernel_version(self.kernel_version)
        print('debug: kernel version =' + self.rest_manager.get_kernel_version())

        path, patch_file = (os.path.split(self.patch))


        # check userID
        data_store = shelve.open('userid')

        # get old userid if present
        try:
            old_userid = data_store['UserID']
        except:
            old_userid = None
            print('no UserID')

        # send uncompressed config and patch files
        replay = self.rest_manager.send_file(self.config, self.patch, file, patch_file, '/elivepatch/api/v1.0/get_files')

        # get userid returned from the server
        userid = replay['get_config']['UserID']
        self.rest_manager.set_user_id(userid)

        # check if the userid is new
        if userid:
            try:
                if userid != old_userid:
                    print('new userid: ' + str(userid))
                    data_store['UserID'] = userid
                    data_store.close()
            except:
                pass

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
        get_file_path = self.path +'/'+self.filename
        store_file_path = '/tmp/'+self.filename
        print('file_path: '+ get_file_path)
        if not os.path.isdir(get_file_path):
            with gzip.open(get_file_path, 'rb') as in_file:
                s = in_file.read()
            # Store uncompressed file
            path_to_store = store_file_path[:-3]  # remove the filename extension
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

