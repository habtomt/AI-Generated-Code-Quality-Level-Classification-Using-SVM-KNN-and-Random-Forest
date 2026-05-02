#!/usr/bin/env python3
import os
import subprocess
import textwrap

APP_NAME = "webapp"
IMAGE_NAME = f"{APP_NAME}:latest"
DEPLOYMENT_FILE = "deployment.yaml"
SERVICE_FILE = "service.yaml"


def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def write_dockerfile():
    dockerfile = textwrap.dedent(f"""
    FROM python:3.11-slim

    WORKDIR /app

    COPY app.py /app/app.py

    RUN pip install flask

    EXPOSE 5000

    CMD ["python", "app.py"]
    """).strip()

    with open("Dockerfile", "w") as f:
        f.write(dockerfile)


def write_app():
    app = textwrap.dedent("""
    from flask import Flask
    import os

    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello from containerized web app!"

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    """).strip()

    with open("app.py", "w") as f:
        f.write(app)


def write_k8s_files():
    deployment = textwrap.dedent(f"""
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: {APP_NAME}-deployment
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: {APP_NAME}
      template:
        metadata:
          labels:
            app: {APP_NAME}
        spec:
          containers:
          - name: {APP_NAME}
            image: {IMAGE_NAME}
            ports:
            - containerPort: 5000
    """).strip()

    service = textwrap.dedent(f"""
    apiVersion: v1
    kind: Service
    metadata:
      name: {APP_NAME}-service
    spec:
      selector:
        app: {APP_NAME}
      ports:
        - protocol: TCP
          port: 80
          targetPort: 5000
      type: LoadBalancer
    """).strip()

    with open(DEPLOYMENT_FILE, "w") as f:
        f.write(deployment)

    with open(SERVICE_FILE, "w") as f:
        f.write(service)


def build_image():
    run(["docker", "build", "-t", IMAGE_NAME, "."])


def deploy_k8s():
    run(["kubectl", "apply", "-f", DEPLOYMENT_FILE])
    run(["kubectl", "apply", "-f", SERVICE_FILE])


def scale_deployment(replicas):
    run([
        "kubectl", "scale", "deployment",
        f"{APP_NAME}-deployment",
        f"--replicas={replicas}"
    ])


def main():
    write_app()
    write_dockerfile()
    write_k8s_files()

    build_image()
    deploy_k8s()

    scale_deployment(3)


if __name__ == "__main__":
    main()