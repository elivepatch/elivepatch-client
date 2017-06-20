#!/usr/bin/env python
import os
from git import Repo
from elivepatch_client.client import restful


class Kernel(object):

    def __init__(self):
        self.minor = 0
        self.major = 0
        self.revision = 0
        self.config = ''
        pass

    def get_version(self):
        tmp = os.uname()[2].split(".")
        self.major = tmp[0]
        self.minor = tmp[1]
        tmp[2] = tmp[2].split("-")
        self.revision = tmp[2][0]
        return self.major, self.minor, self.revision

    def get_config(self, config_path):
        self.config = config_path
        pass

    def send_config(self, url):
        print(str(self.config)+ str(url))
        print (os.path.basename(self.config))
        path, file = (os.path.split(self.config))
        rest_manager = restful.ManaGer(url)
        rest_manager.send_config(self.config, file)
        pass

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
