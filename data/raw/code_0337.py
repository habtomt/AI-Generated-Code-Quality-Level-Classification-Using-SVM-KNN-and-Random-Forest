"""
Auto-generated Python code
Scenario : Cloud Hosting
Prompt   : response_000.txt
Run      : 1
"""

# Import necessary libraries
import os
import subprocess
import yaml

# Function to containerize the application with Docker
def containerize_with_docker(app_name, port):
    """
    Containerize the application with Docker.
    
    Parameters:
    app_name (str): Name of the application.
    port (int): Port number to expose.
    """
    try:
        # Create a Dockerfile
        dockerfile = f"""
        # Use the official lightweight Node.js image
        FROM node:14-alpine

        # Set the working directory
        WORKDIR /usr/src/app

        # Copy package.json and package-lock.json
        COPY package*.json ./

        # Install dependencies
        RUN npm install

        # Bundle app source
        COPY . .

        # Expose the port the app runs on
        EXPOSE {port}

        # Run the application
        CMD ["node", "app.js"]
        """
        with open("Dockerfile", "w") as f:
            f.write(dockerfile)

        # Build the Docker image
        subprocess.run(["docker", "build", "-t", app_name, "."])

        # Run the Docker container locally (optional)
        subprocess.run(["docker", "run", "-p", f"{port}:{port}", app_name])
    except Exception as e:
        print(f"Error containerizing with Docker: {e}")

# Function to prepare for Kubernetes deployment
def prepare_for_kubernetes_deployment(app_name, port):
    """
    Prepare for Kubernetes deployment.
    
    Parameters:
    app_name (str): Name of the application.
    port (int): Port number to expose.
    """
    try:
        # Create a deployment descriptor
        deployment_yaml = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"{app_name}-deployment"
            },
            "spec": {
                "replicas": 3,
                "selector": {
                    "matchLabels": {
                        "app": app_name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": app_name
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": app_name,
                                "image": f"{app_name}:latest",
                                "ports": [
                                    {
                                        "containerPort": port
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        with open("deployment.yaml", "w") as f:
            yaml.dump(deployment_yaml, f)

        # Create a service
        service_yaml = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"{app_name}-service"
            },
            "spec": {
                "type": "LoadBalancer",
                "selector": {
                    "app": app_name
                },
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": port
                    }
                ]
            }
        }
        with open("service.yaml", "w") as f:
            yaml.dump(service_yaml, f)
    except Exception as e:
        print(f"Error preparing for Kubernetes deployment: {e}")

# Function to deploy to Kubernetes
def deploy_to_kubernetes(app_name):
    """
    Deploy to Kubernetes.
    
    Parameters:
    app_name (str): Name of the application.
    """
    try:
        # Apply the deployment and service
        subprocess.run(["kubectl", "apply", "-f", "deployment.yaml"])
        subprocess.run(["kubectl", "apply", "-f", "service.yaml"])

        # Verify the deployment
        subprocess.run(["kubectl", "get", "pods"])
        subprocess.run(["kubectl", "get", "services"])
    except Exception as e:
        print(f"Error deploying to Kubernetes: {e}")

# Function to scale the deployment
def scale_deployment(app_name, replicas):
    """
    Scale the deployment.
    
    Parameters:
    app_name (str): Name of the application.
    replicas (int): Number of replicas.
    """
    try:
        # Scale the deployment
        subprocess.run(["kubectl", "scale", "deployment", f"{app_name}-deployment", "--replicas", str(replicas)])
    except Exception as e:
        print(f"Error scaling deployment: {e}")

# Main function
def main():
    app_name = "my-node-app"
    port = 3000
    replicas = 5

    # Containerize the application with Docker
    containerize_with_docker(app_name, port)

    # Prepare for Kubernetes deployment
    prepare_for_kubernetes_deployment(app_name, port)

    # Deploy to Kubernetes
    deploy_to_kubernetes(app_name)

    # Scale the deployment
    scale_deployment(app_name, replicas)

if __name__ == "__main__":
    main()