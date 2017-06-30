#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import os
from git import Repo
from elivepatch_client.client import restful
import gzip
import os
import os.path


class Kernel(object):

    def __init__(self):
        self.minor = 0
        self.major = 0
        self.revision = 0
        self.config = ''
        self.patch = ''

    def get_version(self):
        tmp = os.uname()[2].split(".")
        self.major = tmp[0]
        self.minor = tmp[1]
        tmp[2] = tmp[2].split("-")
        self.revision = tmp[2][0]
        return self.major, self.minor, self.revision

    def set_config(self, config_path):
        self.config = config_path

    def set_patch(self, patch_path):
        self.patch = patch_path

    def send_config(self, url):
        print('conifg path: '+ str(self.config) + 'server url: ' + str(url))
        print (os.path.basename(self.config))
        path, file = (os.path.split(self.config))
        file_extension = os.path.splitext(file)[1]
        if file_extension == ".gz":
            print('gz extension')
            f_action = FileAction(path, file)
            path, file = f_action.ungz()
            # if the file is .gz the configuration path is the tmp folder uncompressed config file
            self.config = os.path.join(path,file)
        rest_manager = restful.ManaGer(url)
        # we are sending only uncompressed configuration files
        rest_manager.send_file(self.config, file, '/elivepatch/api/v1.0/config')

    def send_patch(self, url):
        print("self.patch: "+ self.patch + ' url: '+url)
        rest_manager = restful.ManaGer(url)
        path, file = (os.path.split(self.patch))
        print('file :'+ file)
        rest_manager.send_file(self.patch, file, '/elivepatch/api/v1.0/patch')

    def build_livepatch(self, url):
        rest_manager = restful.ManaGer(url)
        rest_manager.build_livepatch()

    def get_livepatch(self, url):
        rest_manager = restful.ManaGer(url)
        rest_manager.get_livepatch()


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
            with open(path_to_store, 'w') as f:
                f.write(s)
            print('working')
            path, file = (os.path.split(path_to_store))
        return path, file
