#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, base64
import requests
from requests.auth import HTTPBasicAuth


class ManaGer(object):
    def __init__(self, server_url):
        self.server_url = server_url

    def version(self):
        url = self.server_url + '/elivepatch/api/v1.0/agent'
        r = requests.get(url)
        print(r.text)
        print(r.json())

    def send_file(self, send_file, name_file, api):
        url = self.server_url+ api
        files = {'file': (name_file, open(send_file, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        r = requests.post(url, files=files)

    def build_livepatch(self):
        url = self.server_url+'/elivepatch/api/v1.0/livepatch'
        r = requests.post(url)
        print(r.text)
        print(r.json())