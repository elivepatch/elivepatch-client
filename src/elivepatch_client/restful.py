#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import requests
import os
import shutil
import tempfile
from elivepatch_client import patch
from elivepatch_client import log
import sys
from io import BytesIO


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
        """
        Function for as the server version and print on screen
        """
        url = self.server_url + '/elivepatch/api/v1.0/agent'
        r = requests.get(url)
        log.notice(r.json())

    def send_files(self, temporary_config, new_patch_fullpath, incremental_patches, api):
        """
        Function for send files and build live patch (server side)
        :param temporary_config: configuration file full path
        :param new_patch_fullpath: main patch full path
        :param incremental_patches: List with incremental patches paths
        :param api: RESTFul server path
        :return: json with response
        """
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
        log.notice('incremental_patches: '+str(incremental_patches))
        for incremental_patch_fullpath in incremental_patches:
            if incremental_patch_fullpath.endswith('.patch'):
                # TODO: we need to close what we open
                read_incremental_patch = open(incremental_patch_fullpath, 'rb')
                files.append(('patch', (str(counter).zfill(5) + '.patch', read_incremental_patch, 'multipart/form-data', {'Expires': '0'})))
                counter += 1
        files.append(('main_patch', ('main.patch', open(new_patch_fullpath, 'rb'), 'multipart/form-data', {'Expires': '0'})))
        files.append(('config', ('config', open(temporary_config.name, 'rb'), 'multipart/form-data', {'Expires': '0'})))
        log.notice(str(files))
        try:
            response = requests.post(url, files=files, headers=headers)
            log.notice('send file: ' + str(response.json()))
            response_dict = response.json()
        except requests.exceptions.ConnectionError as e:
            log.notice('connection error: %s' % e)
            temporary_config.close()
        except:
            self._catching_exceptions_exit(self.send_files)
        temporary_config.close()
        return response_dict

    def get_livepatch(self, patch_folder):
        """
        Save the patch in the incremental patches folder and install the livepatch
        :param patch_folder: Main patch that will be saved in the incremental patches folder.
        """
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
                    log.notice(b)
                except:
                    log.notice('livepatch not found')
                    r.close()
        except:
            self._catching_exceptions_exit(self.get_livepatch)

        with tempfile.TemporaryDirectory() as elivepatch_uuid_dir:
            livepatch_fulldir = os.path.join(elivepatch_uuid_dir, 'livepatch.ko')
            if os.path.exists('myfile.ko'):
                if not os.path.exists(elivepatch_uuid_dir):
                    os.makedirs(elivepatch_uuid_dir)
                shutil.copy("myfile.ko", livepatch_fulldir)
                log.notice('livepatch saved in ' + elivepatch_uuid_dir + '/ folder')
                patch_manager.load(patch_folder, livepatch_fulldir)
            else:
                log.notice('livepatch not received')

    def _catching_exceptions_exit(self, current_function):
        e = sys.exc_info()
        log.error( "Error %s: %s" % (current_function.__name__, str(e)) )
        sys.exit(1)
