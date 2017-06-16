#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
import requests

class ManaGer(object):
    def __init__(self,server_url):
        self.server_url = server_url

    def version(self):
        version = json.load(urllib2.urlopen(self.server_url))
        print(version)

    def send_config(self, config_path, config_file):
        url = self.server_url
        headers = {'elivepatch': 'password'}
        files = {'file': (config_file, open(config_path, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        r = requests.post(url, files=files, headers=headers)

