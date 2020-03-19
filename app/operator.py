import argparse
import logging
import sys
import os

from kubernetes import client, config
#from .watcher import *

class watcherOperatorConfig():
    #def __init__(self, customGroup, customVersion, customPlural, customKind, apiVersion, customEventFilter, deployEventFilter):
    def __init__(self):
        self.customGroup = "jabbs19.com"
        self.customVersion = "v1"
        self.customPlural = "watcherconfigs"
        self.customKind = "WatcherConfig"
        self.apiVersion = "CoreV1Api"
        self.customEventFilter =  {'eventTypesList': ['ADDED','MODIFIED','DELETED']}
        self.deployEventFilter = {'eventTypesList': ['zz']}
        self.finalizer = ['watcher.delete.finalizer']

    #     {'eventTypesList': ['ADDED','MODIFIED']}


    #     wcEventTypeList = {'eventTypesList': ['ADDED','MODIFIED']}
    #     wcGroup = watcherOperatorConfig['group']
    # wcVersion = watcherOperatorConfig['version']
    # wcPlural = watcherOperatorConfig['plural']
    # wcKind = watcherOperatorConfig['kind']


    #         watcherOperatorConfig = {
    #             "group": "jabbs19.com",
    #             "version": "v1",
    #             "plural": "watcherconfigs",
    #             "kind": "WatcherConfig",
    #             "k8sApiVersion": "CoreV1Api"
    #                     }    

    # # Changing this it's possible to work on all the namespaces or choose only one
    # deployEventTypeList = {'eventTypesList': ['MODIFIED']}
    # #deployEventTypeList = {'eventTypesList': ['zz']}


    # deploy_watcher = ThreadedWatcher(deployAPI.list_deployment_for_all_namespaces, deployEventTypeList)

    # wcEventTypeList = {'eventTypesList': ['ADDED','MODIFIED']}
    # wcGroup = watcherOperatorConfig['group']
    # wcVersion = watcherOperatorConfig['version']
    # wcPlural = watcherOperatorConfig['plural']
    # wcKind = watcherOperatorConfig['kind']
