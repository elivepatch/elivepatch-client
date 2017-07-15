#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import requests
import os
import shutil


class ManaGer(object):
    """
    RESTful client functions
    """

    def __init__(self, server_url, kernel_version, uuid):
        self.server_url = server_url
        self.kernel_version = kernel_version
        # universally unique identifier for multi-threading
        self.uuid = uuid

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_kernel_version(self, kernel_version):
        self.kernel_version = kernel_version

    def get_kernel_version(self):
        return self.kernel_version

    def get_uuid(self):
        return self.uuid

    def version(self):
        url = self.server_url + '/elivepatch/api/v1.0/agent'
        r = requests.get(url)
        print(r.json())

    def send_file(self, config_send_file, patch_send_file, config_file_name, patch_file_name, api):
        url = self.server_url+ api
        # we are sending the file and the UUID
        # The server is dividing user by UUID
        # UUID is generated with python UUID
        # TODO: add the UUID in the json location instead of headers
        headers = {
            'KernelVersion' : self.kernel_version,
            'UUID': self.uuid
        }
        files = {'patch': (patch_file_name, open(patch_send_file, 'rb'), 'multipart/form-data', {'Expires': '0'}),
                 'config': (config_file_name, open(config_send_file, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        print(str(files))
        r = requests.post(url, files=files, headers=headers)
        print('send file: ' + str(r.json()))
        r_dict = r.json()
        return r_dict

    def build_livepatch(self):
        url = self.server_url+'/elivepatch/api/v1.0/build_livepatch'
        payload = {
            'KernelVersion': self.kernel_version,
            'UUID' : self.uuid
        }
        r = requests.post(url, json=payload)
        print(r.json())

    def get_livepatch(self):
        from io import BytesIO
        url = self.server_url+'/elivepatch/api/v1.0/send_livepatch'
        payload = {
            'KernelVersion': self.kernel_version,
            'UUID' : self.uuid
        }
        r = requests.get(url, json=payload)
        if r.status_code == requests.codes.ok:  # livepatch returned ok
            try:
                b= BytesIO(r.content)
                with open('myfile.ko', 'wb') as out:
                    out.write(r.content)
                r.close()
                print(b)
            except:
                print('livepatch not found')
                r.close()

        elivepatch_uuid_dir = os.path.join('..', 'elivepatch-'+ self.uuid)
        if not os.path.exists(elivepatch_uuid_dir):
            os.makedirs(elivepatch_uuid_dir)
        shutil.move("myfile.ko", os.path.join(elivepatch_uuid_dir, 'livepatch.ko'))
