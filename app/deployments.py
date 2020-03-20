"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""
import logging

from kubernetes import client, config
from kubernetes.client.rest import ApiException

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

def create_deployment_object(watcherApplicationName, fullJSONSpec):

    watcherAppName = watcherApplicationName
    deployNamespace = fullJSONSpec['deployNamespace']
    watchNamespace = fullJSONSpec['watchNamespace']
    k8sApiVersion = fullJSONSpec['k8sApiVersion']
    k8sApiResourceName = fullJSONSpec['k8sApiResourceName']
    annotationFilterBoolean = fullJSONSpec['annotationFilterBoolean']
    annotationFilterString = fullJSONSpec['annotationFilterString']
    eventTypeFilter = fullJSONSpec['eventTypeFilter']
    
    # Configureate Pod template container
    container = client.V1Container(
        name="watcher",
        image="openshift/hello-openshift",
        ports=[client.V1ContainerPort(container_port=8080)],
        env=[client.V1EnvVar(name='ANNOTATION_FILTER_BOOLEAN',value=annotationFilterBoolean),
            client.V1EnvVar(name='ANNOTATION_FILTER_STRING',value=annotationFilterString),
            client.V1EnvVar(name='WATCH_NAMESPACE',value=watchNamespace),
            client.V1EnvVar(name='API_VERSION',value=k8sApiVersion),
            client.V1EnvVar(name='API_RESOURCE_NAME',value=k8sApiResourceName),
            client.V1EnvVar(name='PATH_TO_CA_PEM',value='/ca/route'),   #Figure out later.
            client.V1EnvVar(name='JWT_TOKEN',value='141819048109481094')    #Figure out later.
            ]
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": watcherAppName}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'app': watcherAppName}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=watcherAppName),
        spec=spec)
    return deployment

def create_deployment(apiInstance, deploymentBody, deploymentNamespace):
    # Create deployement
    try:
        api_response = apiInstance.create_namespaced_deployment(body=deploymentBody,namespace=deploymentNamespace)
        logger.info("Deployment Created [" + api_response.metadata.name +"]")
    except ApiException as e:
        logger.error("Deployment not created. [Deployment: " + api_response.metadata.name + "][CREATE] Error: %s\n" % e)


def update_deployment(apiInstance, deploymentBody, deploymentName, deploymentNamespace):
    # Patch the deployment
    try:
        api_response = apiInstance.patch_namespaced_deployment(name=deploymentName,namespace=deploymentNamespace,body=deploymentBody)
        logger.info("Deployment Patched [" + deploymentName +"]")
    except ApiException as e:
        logger.error("Deployment not patched. [Deployment: " + deploymentName + "][PATCH] Error: %s\n" % e)


def delete_deployment(apiInstance, deploymentName, deploymentNamespace):
    # Delete deployment
    try:
        api_response = apiInstance.delete_namespaced_deployment(name=deploymentName, namespace=deploymentNamespace, body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
        logger.info("Deployment Deleted [" + deploymentName +"]")
    except ApiException as e:
        logger.error("Deployment not patched. [Deployment: " + deploymentName + "][DELETE] Error: %s\n" % e)


def check_for_deployment(apiInstance, deploymentName, deploymentNamespace):
    try:
        api_response = apiInstance.read_namespaced_deployment(name=deploymentName, namespace=deploymentNamespace)
        return True
    except ApiException as e:
        return False

