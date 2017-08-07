#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import requests
import os
import shutil
from elivepatch_client.client import patch
import sys


class ManaGer(object):
    """
    RESTful client functions
    """

    def __init__(self, server_url, kernel_version, uuid):
        self.server_url = server_url
        self.kernel_version = kernel_version
        # universally unique identifier for support multiple request
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

    def send_files(self, temporary_config, new_patch_fullpath, incremental_patches, api):
        url = self.server_url+ api
        # we are sending the file and the UUID
        # The server is dividing user by UUID
        # UUID is generated with python UUID
        # TODO: add the UUID in the json location instead of headers
        response_dict = None
        headers = {
            'KernelVersion' : self.kernel_version,
            'UUID': self.uuid
        }
        # Static patch and config filename
        files=[]
        counter = 0
        for incremental_patch_fullpath in incremental_patches:
            read_incremental_patch = open(incremental_patch_fullpath, 'rb')
            files.append(('patch', (str(counter) + '.patch', read_incremental_patch, 'multipart/form-data', {'Expires': '0'})))
            read_incremental_patch.close()
            counter += 1
        files.append(('main_patch', ('main_patch', open(new_patch_fullpath, 'rb'), 'multipart/form-data', {'Expires': '0'})))
        files.append(('config', ('config', open(temporary_config.name, 'rb'), 'multipart/form-data', {'Expires': '0'})))
        print(str(files))
        temporary_config.close()
        try:
            response = requests.post(url, files=files, headers=headers)
            print('send file: ' + str(response.json()))
            response_dict = response.json()
        except requests.exceptions.ConnectionError as e:
            print('connection error: %s' % e)
            sys.exit(1)
        #except:
            #self.catching_exceptions_exit(self.send_file)
        return response_dict

    def build_livepatch(self):
        url = self.server_url+'/elivepatch/api/v1.0/build_livepatch'
        payload = {
            'KernelVersion': self.kernel_version,
            'UUID' : self.uuid
        }
        try:
            response = requests.post(url, json=payload)
            print(response.json())
        except:
            self._catching_exceptions_exit(self.build_livepatch)

    def get_livepatch(self, patch_folder):
        from io import BytesIO
        patch_manager = patch.ManaGer()
        url = self.server_url+'/elivepatch/api/v1.0/send_livepatch'
        payload = {
            'KernelVersion': self.kernel_version,
            'UUID' : self.uuid
        }
        try:
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
        except:
            self._catching_exceptions_exit(self.get_livepatch)

        elivepatch_uuid_dir = os.path.join('..', 'elivepatch-'+ self.uuid)
        livepatch_fulldir = os.path.join(elivepatch_uuid_dir, 'livepatch.ko')
        if os.path.exists('myfile.ko'):
            if not os.path.exists(elivepatch_uuid_dir):
                os.makedirs(elivepatch_uuid_dir)
            shutil.copy("myfile.ko", livepatch_fulldir)
            print('livepatch saved in ' + elivepatch_uuid_dir + '/ folder')
            patch_manager.load(patch_folder, livepatch_fulldir)
        else:
            print('livepatch not received')

    def _catching_exceptions_exit(self, current_function):
        e = sys.exc_info()
        print( "Error %s: %s" % (current_function.__name__, str(e)) )
        sys.exit(1)