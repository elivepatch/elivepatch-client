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
        url = self.server_url+'/elivepatch/api/v1.0/build_livepatch'
        payload = {
                    'KernelVersion': '4.10.16'
        }
        r = requests.post(url, json=payload)
        print(r.text)
        print(r.json())

    def get_livepatch(self):
        url = self.server_url+'/elivepatch/api/v1.0/get_livepatch'
        payload = {
            'KernelVersion': '4.10.16'
        }
        r = requests.post(url, json=payload)
        print(r.text)
        print(r.json())