import argparse
import logging
import sys
import os

from kubernetes import client, config
#from .watcher import *

from  .defs import *
from .controller import Controller
from .threadedwatch import ThreadedWatcher
from .clientconfig import *
from .watcher import *
from .operator import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():

    #Cluster "client" configuration
    cc = clientconfig()
   
    #Create API Instances for Deployment "Watcher" and the WatcherConfig "Watcher"
    deployAPI = client.AppsV1Api(cc.authConfiguration)
    customAPI = client.CustomObjectsApi(cc.authConfiguration)


    #WatcherOperatorConfig "Master" Configuration (Could be configmap, secret, helm values, etc.)
    #Change into CRD, run an "install Pod" to do upgrades, installs, etc.

    #Operator Config
    watchOpConfig = watcherOperatorConfig()
    
    deployment_watcher = ThreadedWatcher(deployAPI.list_deployment_for_all_namespaces, watchOpConfig.deployEventFilter)


    #Application Configs

    config_watcher = ThreadedWatcher(customAPI.list_cluster_custom_object, 
                                            watchOpConfig.customEventFilter,
                                            watchOpConfig.customGroup, 
                                            watchOpConfig.customVersion, 
                                            watchOpConfig.customPlural)

    controller = Controller(cc.authConfiguration, deployment_watcher, config_watcher, deployAPI, customAPI,
                            watchOpConfig,
                            watchOpConfig.customGroup,
                            watchOpConfig.customVersion,
                            watchOpConfig.customPlural,
                            watchOpConfig.customKind)


    controller.start()
    deployment_watcher.start()
    config_watcher.start()
    try:
        controller.join()
    except (KeyboardInterrupt, SystemExit):
        print('\n! Received keyboard interrupt, quitting threads.\n')
        controller.stop()
        controller.join()


if __name__ == '__main__':
    main()
