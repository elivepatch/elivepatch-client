#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, base64
try:
    import urllib
except:
    import urllib.request as urllib
import requests

class ManaGer(object):
    def __init__(self, server_url):
        self.server_url = server_url
        self.version()

    def version(self):

        # If you access to url below via Proxy,
        # set environment variable 'http_proxy' before execute this.
        # And, url scheme is https, then 'https_proxy' must be set instead of 'http_proxy'
        url = self.server_url + '/elivepatch/api/v1.0/agent'

        # https://docs.python.org/3/library/functions.html#input
        # https://docs.python.org/3/library/getpass.html
        auth_user='elivepatch'
        auth_passwd='default'

        # https://docs.python.org/3.4/howto/urllib2.html#id5
        #
        # If you would like to request Authorization header for Digest Authentication,
        # replace HTTPBasicAuthHandler object to HTTPDigestAuthHandler
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, auth_user, auth_passwd)
        authhandler = urllib.request.HTTPBasicAuthHandler(passman)
        opener = urllib.request.build_opener(authhandler)
        urllib.request.install_opener(opener)

        # I can get http.client.HTTPResponse object in variable 'res'
        # https://docs.python.org/3/library/http.client.html#httpresponse-objects
        #
        # ToDo: Error Handling
        # https://docs.python.org/3/howto/urllib2.html#handling-exceptions
        res = urllib.request.urlopen(url)
        res_body = res.read()
        print(res_body.decode('utf-8'))

    def send_config(self, config_path, config_file):
        url = self.server_url
        headers = {'elivepatch': 'password'}
        files = {'file': (config_file, open(config_path, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        r = requests.post(url, files=files, headers=headers)

