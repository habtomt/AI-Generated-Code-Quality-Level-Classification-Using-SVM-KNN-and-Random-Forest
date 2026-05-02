#!/usr/bin/env python3
"""
container_security_guard.py
"""

import time
import random
import uuid


class Container:
    def __init__(self, name, image):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.image = image
        self.running = True
        self.vulnerabilities = self.scan_image()

    def scan_image(self):
        return random.sample(
            ["CVE-2024-001", "CVE-2024-002", "CVE-2024-003", "NONE"],
            k=random.randint(1, 2)
        )

    def is_secure(self):
        return "NONE" in self.vulnerabilities and len(self.vulnerabilities) == 1


class NetworkPolicy:
    def __init__(self):
        self.allowed_pairs = set()

    def allow(self, src, dst):
        self.allowed_pairs.add((src, dst))

    def is_allowed(self, src, dst):
        return (src, dst) in self.allowed_pairs


class RBAC:
    def __init__(self):
        self.roles = {}

    def assign_role(self, user, role):
        self.roles[user] = role

    def check_access(self, user, action):
        role = self.roles.get(user)
        if role == "admin":
            return True
        if role == "dev" and action in ["read", "deploy"]:
            return True
        if role == "viewer" and action == "read":
            return True
        return False


class SecurityScanner:
    def scan(self, container):
        print(f"[SCAN] {container.name}-{container.id}: {container.vulnerabilities}")
        return container.is_secure()


class SecurityManager:
    def __init__(self):
        self.scanner = SecurityScanner()
        self.network = NetworkPolicy()
        self.rbac = RBAC()
        self.containers = []

    def deploy_container(self, user, container):
        if not self.rbac.check_access(user, "deploy"):
            print(f"[RBAC DENY] {user} cannot deploy containers")
            return

        if not self.scanner.scan(container):
            print(f"[SECURITY BLOCK] Vulnerable container {container.id}")
            return

        self.containers.append(container)
        print(f"[DEPLOYED] {container.name}-{container.id}")

    def send_request(self, src, dst):
        if not self.network.is_allowed(src, dst):
            print(f"[NETWORK BLOCK] {src} -> {dst}")
            return
        print(f"[NETWORK OK] {src} -> {dst}")


def main():
    sec = SecurityManager()

    sec.rbac.assign_role("alice", "admin")
    sec.rbac.assign_role("bob", "dev")
    sec.rbac.assign_role("eve", "viewer")

    sec.network.allow("service-a", "service-b")

    c1 = Container("api-service", "nginx:latest")
    c2 = Container("db-service", "postgres:alpine")

    sec.deploy_container("alice", c1)
    sec.deploy_container("bob", c2)
    sec.deploy_container("eve", c1)

    time.sleep(1)

    sec.send_request("service-a", "service-b")
    sec.send_request("service-b", "service-a")


if __name__ == "__main__":
    main()