import argparse
import logging
import sys
import os

from kubernetes import client, config
from kubernetes.client import rest

#from .watcher import *


class clientconfig():
    def __init__(self, sslCertPath=None, jwtTOKEN=None, **kwargs):
        self.sslCertPath = sslCertPath
        self.jwtTOKEN = jwtTOKEN
        self.kwargs = kwargs


        if 'KUBERNETES_PORT' in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()
            
        # create an instance of the API class
        authConfiguration = client.Configuration()

         # Logging Settings
        #authConfiguration.logger = {}
        #authConfiguration.logger["package_logger"] = logging.getLogger("client")

        #authConfiguration = None
        #authConfiguration.verify_ssl = False
        #authConfiguration.api_key_prefix['attribute'] = 'default_headers'
        #authConfiguration.api_key["attribute"] = 'yes'

        #authConfiguration.ssl_ca_cert = os.getenv('PATH_TO_CA_PEM')
        #authConfiguration.api_key_prefix['authorization'] = 'Bearer'
        #uthConfiguration.api_key["authorization"] = jwtTOKEN
        self.authConfiguration = authConfiguration
