import argparse
import logging
import sys
import os

from kubernetes import client, config
from kubernetes.client.rest import ApiException
from .customresources import *
#from .watcher import *

class watcherApplication():
    def __init__(self, apiInstance, crObject, operatorConfig):
        self.apiInstance = apiInstance

        #Unpack Object (See how to use self.crObject.customGroup)
        self.operatorConfig = operatorConfig
        self.customGroup = operatorConfig.customGroup
        self.customVersion = operatorConfig.customVersion
        self.customPlural = operatorConfig.customPlural
        self.customKind = operatorConfig.customKind

        self.watcherApplicationName = crObject['metadata']['name']
        self.deployNamespace = None
        self.watchNamespace = None
        self.k8sApiVersion = None
        self.k8sApiResourceName = None
        self.annotationFilterBoolean = None
        self.annotationFilterString = None
        self.eventTypeFilter = None
        self.fullJSONSpec = None
        self.status = None
        self.deleteTimestamp = None

        #Extract CR Object
        self.deployNamespace = crObject['spec']['deployNamespace']
        self.watchNamespace = crObject['spec']['watchNamespace']
        self.k8sApiVersion = crObject['spec']['k8sApiVersion']
        self.k8sApiResourceName = crObject['spec']['k8sApiResourceName']
        self.annotationFilterBoolean = crObject['spec']['annotationFilterBoolean']
        self.annotationFilterString = crObject['spec']['annotationFilterString']
        self.eventTypeFilter = crObject['spec']['eventTypeFilter']
        self.fullJSONSpec = crObject['spec']

    def update_status(self, newStatus):
        currentConfig = get_custom_resource(self.apiInstance, self.customGroup, self.customVersion, self.customPlural, self.watcherApplicationName)
        #Check by printing this.  
        #Overwrite the "status"
        #currentConfig.metadata.status = newStatus

        #Patch the actual resource.
        api_response = patch_custom_resource(self.apiInstance, self.customGroup, self.customVersion, self.customPlural, self.customKind, self.watcherApplicationName, currentConfig)
        return api_response
    
    def check_marked_for_delete(self):
        try:
            currentConfig = get_custom_resource(self.apiInstance, self.customGroup, self.customVersion, self.customPlural, self.watcherApplicationName)
            self.deleteTimestamp = currentConfig['metadata']['deletionTimestamp']
            return True
        except:
            self.deleteTimestamp = None
            return False
        
    def remove_finalizer(self):
        #Build Body to pass to customresources.patch
        noFinalizerBody = {
        "apiVersion": self.customGroup + '/' + self.customVersion,
        "kind": self.customKind,
        "metadata": {
            "name": self.watcherApplicationName,
            "finalizers": []
                    }
        }
    
        api_response = patch_custom_resource(self.apiInstance, self.customGroup, self.customVersion, self.customPlural, self.customKind, self.watcherApplicationName, noFinalizerBody)
 
    # def removeFinalizer(self, operatorConfigObject, apiInstance, watcherConfigName):
    #         body = ""
    #         api_response = apiInstance.patch_cluster_custom_object(operatorConfigObject.customGroup, 
    #                                                             operatorConfigObject.customVersion, 
    #                                                             operatorConfigObject.customPlural, 
    #                                                             watcherConfigName,
    #                                                             body
    
        
    #     self.operatorConfigObject = operatorConfigObject
    #     self.apiInstance = apiInstance
    #     try:
    #         api_response = self.apiInstance.get_cluster_custom_object(self.operatorConfigObject.customGroup, 
    #                                                             self.operatorConfigObject.customVersion, 
    #                                                             self.operatorConfigObject.customPlural,
    #                                                             watcherConfigName)
    #         self.watcherApplicationName = watcherConfigName
    #         self.deployNamespace = api_response['spec']['deployNamespace']
    #         self.watchNamespace = api_response['spec']['watchNamespace']
    #         self.k8sApiVersion = api_response['spec']['k8sApiVersion']
    #         self.k8sApiResourceName = api_response['spec']['k8sApiResourceName']
    #         self.annotationFilterBoolean = api_response['spec']['annotationFilterBoolean']
    #         self.annotationFilterString = api_response['spec']['annotationFilterString']
    #         self.eventTypeFilter = api_response['spec']['eventTypeFilter']
    #         self.fullJSONSpec = api_response['spec']
            
    #     except ApiException as e:
    #         self.watcherApplicationName = None
    #         self.deployNamespace = None
    #         self.watchNamespace = None
    #         self.k8sApiVersion = None
    #         self.k8sApiResourceName = None
    #         self.annotationFilterBoolean = None
    #         self.annotationFilterString = None
    #         self.eventTypeFilter = None
    #         self.fullJSONSpec = None
    #         self.status = None
    #         print("No watcher config object found.")

   
    
    # def updateStatus(self, watcherConfigName, status):
    #     self.status = status

    # def checkForApplicationConfig(self, operatorConfigObject, apiInstance, watcherConfigName):
    #     try:
    #         api_response = self.apiInstance.get_cluster_custom_object(operatorConfigObject.customGroup, 
    #                                                             operatorConfigObject.customVersion, 
    #                                                             operatorConfigObject.customPlural, 
    #                                                             watcherConfigName)
    #         #print(api_response)                                                                
    #         return True
    #     except:
    #         return False  


            #print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)  

    # def checkForApplicationConfig(self, watcherConfigName):
    #     try:
    #         api_response = self.apiInstance.get_cluster_custom_object(operatorConfigObject.customGroup, 
    #                                                             operatorConfigObject.customVersion, 
    #                                                             operatorConfigObject.customPlural, 
    #                                                             watcherConfigName)
    #         print(api_response)                                                                
    #         return True
    #     except:
    #         return False               

    # def _getConfiguration(self):
    #     # create an instance of the API class
    #     configuration = client.Configuration()
    #     configuration.api_key_prefix['select_header_accept'] = 'Yes'

    #     #configuration.ssl_ca_cert = os.getenv('PATH_TO_CA_PEM')
    #     #configuration.api_key_prefix['authorization'] = 'Bearer'
    #     #configuration.api_key["authorization"] = os.getenv('JWT_TOKEN')
    #     return configuration

    # def _getWatcherConfigObject(self, wcName):
    #     # create an instance of the API class
    #     configuration = client.Configuration()
    #     #configuration.ssl_ca_cert = os.getenv('PATH_TO_CA_PEM')
    #     #configuration.api_key_prefix['authorization'] = 'Bearer'
    #     #configuration.api_key["authorization"] = os.getenv('JWT_TOKEN')

    # # create an instance of the API class
    #     apiInstance = client.CustomObjectsApi(client.ApiClient(configuration))
        
    #     try:
    #         api_response = apiInstance.get_cluster_custom_object(self.customGroup, self.customVersion, self.customPlural, wcName)
    #         return(api_response)
    #     except ApiException as e:
    #         print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)     

    # def _getWatcherConfigObject(self, wcName):
   
    #     apiInstance = client.CustomObjectsApi(self.authconfiguration)
        
    #     try:
    #         api_response = apiInstance.get_cluster_custom_object(self.customGroup, self.customVersion, self.customPlural, wcName)
    #         return(api_response)
    #     except ApiException as e:
    #         print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)                 