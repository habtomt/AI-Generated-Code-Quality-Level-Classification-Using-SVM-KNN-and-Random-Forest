"""
Auto-generated Python code
Scenario : Container Orchestration
Prompt   : response_000.txt
Run      : 3
"""

# Import required libraries
import os
import sys
from kubernetes import client, config
from kubernetes.client import Configuration

# Create a Kubernetes configuration object
def get_kube_config():
    try:
        # Load the Kubernetes configuration from the default location
        config.load_kube_config()
    except Exception as e:
        # If the default configuration is not found, create a new configuration with a service account token
        config.load_incluster_config()
        # Configure the Kubernetes client
        Configuration.host = os.environ.get('KUBECONFIG')
        Configuration.api_key = {'Bearer': os.environ.get('KUBE_TOKEN')}

# Create a Kubernetes client object
def create_kube_client():
    get_kube_config()
    return client.ApiClient(configuration=Configuration())

# Define a function to deploy an application to a Kubernetes cluster
def deploy_app(app_name, image_name, namespace, replicas):
    kube_client = create_kube_client()
    v1 = client.AppsV1Api(kube_client)
    
    # Create a new deployment
    deployment = client.V1Deployment(
        api_version='apps/v1',
        kind='Deployment',
        metadata=client.V1ObjectMeta(name=app_name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels={'app': app_name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={'app': app_name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name=app_name,
                        image=image_name,
                        ports=[client.V1ContainerPort(container_port=80)],
                    )],
                ),
            ),
        ),
    )
    
    try:
        # Create the deployment in the specified namespace
        v1.create_namespaced_deployment(namespace=namespace, body=deployment)
        print(f"Deployment {app_name} created successfully in namespace {namespace}")
    except client.rest.ApiException as e:
        print(f"Error creating deployment: {e.status}")
        sys.exit(1)

# Define a function to scale an existing deployment
def scale_deployment(app_name, namespace, replicas):
    kube_client = create_kube_client()
    v1 = client.AppsV1Api(kube_client)
    
    try:
        # Get the existing deployment
        deployment = v1.read_namespaced_deployment(app_name, namespace)
        
        # Update the number of replicas
        deployment.spec.replicas = replicas
        
        # Update the deployment
        v1.patch_namespaced_deployment(app_name, namespace, {'spec': deployment.spec})
        print(f"Deployment {app_name} scaled successfully to {replicas} replicas in namespace {namespace}")
    except client.rest.ApiException as e:
        print(f"Error scaling deployment: {e.status}")
        sys.exit(1)

# Define a function to delete a deployment
def delete_deployment(app_name, namespace):
    kube_client = create_kube_client()
    v1 = client.AppsV1Api(kube_client)
    
    try:
        # Delete the deployment in the specified namespace
        v1.delete_namespaced_deployment(app_name, namespace)
        print(f"Deployment {app_name} deleted successfully in namespace {namespace}")
    except client.rest.ApiException as e:
        print(f"Error deleting deployment: {e.status}")
        sys.exit(1)

# Example usage
if __name__ == "__main__":
    # Set the Kubernetes configuration environment variables
    os.environ['KUBECONFIG'] = '/path/to/kubeconfig'
    os.environ['KUBE_TOKEN'] = 'Bearer YOUR_KUBE_TOKEN'
    
    # Deploy an application to a Kubernetes cluster
    app_name = 'my-app'
    image_name = 'your-image-name'
    namespace = 'default'
    replicas = 3
    deploy_app(app_name, image_name, namespace, replicas)
    
    # Scale the deployment
    scale_deployment(app_name, namespace, 5)
    
    # Delete the deployment
    delete_deployment(app_name, namespace)