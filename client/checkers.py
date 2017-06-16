#!/usr/bin/env python
import os
from git import Repo


class Kernel():

    def __init__(self):
        self.minor = 0
        self.major = 0
        self.revision = 0
        pass

    def get_version(self):
        tmp = os.uname()[2].split(".")
        self.major = tmp[0]
        self.minor = tmp[1]
        tmp[2] = tmp[2].split("-")
        self.revision = tmp[2][0]
        pass


class CVE():

    def __init__(self):
        self.git_url = "https://github.com/nluedtke/linux_kernel_cves"
        self.repo_dir = "/tmp/kernel_cve/"
        pass

    def download(self):
        Repo.clone_from(self.git_url, self.repo_dir)

    def set_repo(self, git_url, repo_dir):
        self.git_url = git_url
        self.repo_dir = repo_dir
