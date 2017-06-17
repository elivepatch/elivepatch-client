#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, base64
import requests
from requests.auth import HTTPBasicAuth

class ManaGer(object):
    def __init__(self, server_url):
        self.server_url = server_url
        self.version()

    def version(self):
        url = self.server_url + '/elivepatch/api/v1.0/agent'
        auth_user='elivepatch'
        auth_passwd='default'
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        print(r.text)
        print(r.json())

    def send_config(self, config_path, config_file):
        url = self.server_url
        headers = {'elivepatch': 'password'}
        files = {'file': (config_file, open(config_path, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        r = requests.post(url, files=files, headers=headers)

