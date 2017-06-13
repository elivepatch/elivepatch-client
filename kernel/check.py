#!/usr/bin/env python
import os


class KernelCheck():
    def __init__(self):
        pass

    def version(self):

        for i in os.uname():
            print(i)
        pass
