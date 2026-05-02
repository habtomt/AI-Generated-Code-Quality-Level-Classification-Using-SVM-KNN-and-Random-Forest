"""
Auto-generated Python code
Scenario : Container Orchestration
Prompt   : response_003.txt
Run      : 2
"""

# Required imports
import os
import subprocess
import json
import docker
from kubernetes import client, config

# Set environment variables
STAGING_NAMESPACE = "staging"
PRODUCTION_NAMESPACE = "production"
IMAGE_REPOSITORY = "your-image-repository"
IMAGE_TAG = "your-image-tag"

# Load Kubernetes configuration
try:
    config.load_kube_config()
except Exception as e:
    print(f"Error loading Kubernetes configuration: {e}")
    exit(1)

# Create Kubernetes API clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

# Define a function to update a deployment
def update_deployment(namespace, deployment_name, image):
    # Get the current deployment
    try:
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
    except client.ApiException as e:
        print(f"Error reading deployment: {e}")
        return False

    # Update the deployment image
    deployment.spec.template.spec.containers[0].image = image

    try:
        # Patch the deployment with the new image
        apps_v1.patch_namespaced_deployment(deployment_name, namespace, deployment)
    except client.ApiException as e:
        print(f"Error patching deployment: {e}")
        return False

    return True

# Define a function to roll out a new deployment
def rollout_deployment(namespace, deployment_name, new_image):
    # Roll out a new deployment
    rollout = client.RolloutRolloutStrategy(
        type="Recreate",
        rollingUpdate=client.RollingUpdateDeploymentRollingUpdate(
            maxUnavailable=1
        )
    )

    # Create a new deployment with the new image
    new_deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name=deployment_name,
            namespace=namespace
        ),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": deployment_name}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="app",
                            image=new_image
                        )
                    ]
                )
            ),
            strategy=rollout
        )
    )

    # Patch the existing deployment to use the new rollout strategy
    try:
        apps_v1.patch_namespaced_deployment_deployment(strategy=rollout, name=deployment_name, namespace=namespace)
    except client.ApiException as e:
        print(f"Error patching deployment: {e}")
        return False

    # Create the new deployment
    try:
        apps_v1.create_namespaced_deployment(namespace=namespace, body=new_deployment)
    except client.ApiException as e:
        print(f"Error creating new deployment: {e}")
        return False

    return True

# Update and roll out the staging and production deployments
if update_deployment(STAGING_NAMESPACE, "staging-app", f"{IMAGE_REPOSITORY}:{IMAGE_TAG}") and rollout_deployment(STAGING_NAMESPACE, "staging-app", f"{IMAGE_REPOSITORY}:{IMAGE_TAG}"):
    print("Staging deployment updated and rolled out successfully")
else:
    print("Staging deployment update and roll out failed")

if update_deployment(PRODUCTION_NAMESPACE, "prod-app", f"{IMAGE_REPOSITORY}:{IMAGE_TAG}") and rollout_deployment(PRODUCTION_NAMESPACE, "prod-app", f"{IMAGE_REPOSITORY}:{IMAGE_TAG}"):
    print("Production deployment updated and rolled out successfully")
else:
    print("Production deployment update and roll out failed")