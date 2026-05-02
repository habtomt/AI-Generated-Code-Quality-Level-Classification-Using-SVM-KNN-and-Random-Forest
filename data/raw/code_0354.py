"""
Auto-generated Python code
Scenario : Container Orchestration
Prompt   : response_002.txt
Run      : 1
"""

import os
import subprocess
import time
from kubernetes import client, config
from kubernetes.client import Configuration

# Load Kubernetes configuration
config.load_kube_config()

# Create Kubernetes API clients
apps_v1 = client.AppsV1Api()
autoscaling_v1 = client.AutoscalingV1Api()
autoscaling_v2 = client.AutoscalingV2Api()
core_v1 = client.CoreV1Api()

def create_deployment(name, image):
    """
    Create a Kubernetes Deployment.
    """
    # Define the Deployment specification
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": name}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name=name,
                        image=image,
                        resources=client.V1ResourceRequirements(
                            requests={"cpu": "100m", "memory": "128Mi"},
                            limits={"cpu": "200m", "memory": "256Mi"}
                        )
                    )]
                )
            )
        )
    )
    # Create the Deployment
    apps_v1.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )

def create_horizontal_pod_autoscaler(name, deployment_name):
    """
    Create a Kubernetes Horizontal Pod Autoscaler.
    """
    # Define the HPA specification
    hpa = client.AutoscalingV2beta2HorizontalPodAutoscaler(
        api_version="autoscaling/v2",
        kind="HorizontalPodAutoscaler",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.AutoscalingV2beta2HorizontalPodAutoscalerSpec(
            scale_target_ref=client.V2beta2CrossVersionObjectReference(
                api_version="apps/v1",
                kind="Deployment",
                name=deployment_name
            ),
            min_replicas=1,
            max_replicas=10,
            metrics=[client.AutoscalingV2beta2MetricSpec(
                type="Resource",
                resource=client.AutoscalingV2beta2ResourceMetricSource(
                    name="cpu",
                    target=client.AutoscalingV2beta2MetricTarget(
                        type="Utilization",
                        average_utilization=50
                    )
                )
            )]
        )
    )
    # Create the HPA
    autoscaling_v2.create_namespaced_horizontal_pod_autoscaler(
        namespace="default",
        body=hpa
    )

def create_vertical_pod_autoscaler(name, deployment_name):
    """
    Create a Kubernetes Vertical Pod Autoscaler.
    """
    # Define the VPA specification
    vpa = client.AutoscalingV1VerticalPodAutoscaler(
        api_version="autoscaling.k8s.io/v1",
        kind="VerticalPodAutoscaler",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.AutoscalingV1VerticalPodAutoscalerSpec(
            target=client.AutoscalingV1CrossVersionObjectReference(
                api_version="apps/v1",
                kind="Deployment",
                name=deployment_name
            ),
            update_policy=client.AutoscalingV1PodUpdatePolicy(
                update_mode="Auto"
            )
        )
    )
    # Create the VPA
    autoscaling_v1.create_namespaced_vertical_pod_autoscaler(
        namespace="default",
        body=vpa
    )

def install_metrics_server():
    """
    Install Metrics Server.
    """
    # Install Metrics Server using kubectl
    subprocess.run([
        "kubectl",
        "apply",
        "-f",
        "https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
    ])

def main():
    # Set up a Kubernetes cluster
    print("Setting up a Kubernetes cluster...")

    # Create a Deployment
    deployment_name = "myapp"
    image = "nginx:latest"
    create_deployment(deployment_name, image)

    # Create a Horizontal Pod Autoscaler
    hpa_name = "myapp-hpa"
    create_horizontal_pod_autoscaler(hpa_name, deployment_name)

    # Create a Vertical Pod Autoscaler
    vpa_name = "myapp-vpa"
    create_vertical_pod_autoscaler(vpa_name, deployment_name)

    # Install Metrics Server
    install_metrics_server()

    # Monitor autoscaling
    print("Monitoring autoscaling...")
    while True:
        # Get HPA status
        hpa = autoscaling_v2.read_namespaced_horizontal_pod_autoscaler(
            name=hpa_name,
            namespace="default"
        )
        print(f"HPA replicas: {hpa.status.replicas}")

        # Get VPA status
        vpa = autoscaling_v1.read_namespaced_vertical_pod_autoscaler(
            name=vpa_name,
            namespace="default"
        )
        print(f"VPA recommendations: {vpa.status.recommendation}")

        # Wait for 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    main()