import argparse
import logging
import sys
import os

from kubernetes import client, config
#from .watcher import *


class clientconfig():
    def __init__(self, sslCertPath=None, jwtTOKEN=None, **kwargs):
        self.sslCertPath = sslCertPath
        self.jwtTOKEN = jwtTOKEN
        self.kwargs = kwargs

        # create an instance of the API class
        #authConfiguration = client.Configuration()
        authConfiguration = None
        #configuration.verify_ssl = False
        #configuration.api_key_prefix['select_header_accept'] = 'Yes'
        #configuration.default_headers['select_header_accept'] = 'Yes'


        #configuration.ssl_ca_cert = os.getenv('PATH_TO_CA_PEM')
        #configuration.api_key_prefix['authorization'] = 'Bearer'
        #configuration.api_key["authorization"] = os.getenv('JWT_TOKEN')
        self.authConfiguration = authConfiguration

        self._loadKubeConfig()

    def _loadKubeConfig(self):
        if 'KUBERNETES_PORT' in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()