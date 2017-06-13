#!/usr/bin/env python
import os


class Kernel():

    def __init__(self):
        self.minor = 0
        self.major = 0
        self.revision = 0
        pass

    def get_version(self):
        import pprint
        tmp = os.uname()[2].split(".")
        self.major = tmp[0]
        self.minor = tmp[1]
        tmp[2] = tmp[2].split("-")
        self.revision = tmp[2][0]
        pass
