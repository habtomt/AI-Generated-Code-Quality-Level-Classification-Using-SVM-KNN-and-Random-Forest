#!/usr/bin/env python3
"""
multi_cloud_deployer.py
"""

import argparse
import json
import subprocess
import sys
from abc import ABC, abstractmethod


class CloudProvider(ABC):
    @abstractmethod
    def deploy(self, app_name: str, image: str, region: str):
        pass


class AWSProvider(CloudProvider):
    def deploy(self, app_name: str, image: str, region: str):
        print(f"[AWS] Deploying {app_name} in {region} using image {image}")
        cmd = [
            "echo",
            f"aws ecs update-service --cluster {app_name}-cluster --region {region}"
        ]
        subprocess.run(cmd)


class GCPProvider(CloudProvider):
    def deploy(self, app_name: str, image: str, region: str):
        print(f"[GCP] Deploying {app_name} in {region} using image {image}")
        cmd = [
            "echo",
            f"gcloud run deploy {app_name} --image {image} --region {region}"
        ]
        subprocess.run(cmd)


class AzureProvider(CloudProvider):
    def deploy(self, app_name: str, image: str, region: str):
        print(f"[AZURE] Deploying {app_name} in {region} using image {image}")
        cmd = [
            "echo",
            f"az container create --name {app_name} --image {image} --location {region}"
        ]
        subprocess.run(cmd)


class MultiCloudManager:
    def __init__(self):
        self.providers = {
            "aws": AWSProvider(),
            "gcp": GCPProvider(),
            "azure": AzureProvider()
        }

    def deploy(self, config: dict):
        app_name = config["app_name"]
        image = config["image"]
        deployments = config["deployments"]

        for dep in deployments:
            provider_name = dep["provider"]
            region = dep["region"]

            provider = self.providers.get(provider_name.lower())
            if not provider:
                print(f"Unsupported provider: {provider_name}")
                continue

            provider.deploy(app_name, image, region)


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Multi-Cloud Deployment Manager")
    parser.add_argument("--config", required=True, help="Path to deployment config JSON")

    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Failed to load config: {e}")
        sys.exit(1)

    manager = MultiCloudManager()
    manager.deploy(config)


if __name__ == "__main__":
    main()