#!/usr/bin/env python3
"""
zero_downtime_deployment_pipeline.py
"""

import time
import threading
import uuid
import random
from typing import List


class Container:
    def __init__(self, version: str):
        self.id = str(uuid.uuid4())[:8]
        self.version = version
        self.healthy = True

    def run_health_check(self) -> bool:
        return self.healthy and random.random() > 0.05


class Environment:
    def __init__(self, name: str, replicas: int):
        self.name = name
        self.replicas = [Container("v1.0") for _ in range(replicas)]
        self.lock = threading.Lock()

    def status(self):
        return [(c.id, c.version, c.healthy) for c in self.replicas]


class DeploymentPipeline:
    def __init__(self, env: Environment):
        self.env = env

    def build(self, version: str):
        print(f"[BUILD] Building version {version}")
        time.sleep(1)
        return version

    def test(self, version: str):
        print(f"[TEST] Testing version {version}")
        time.sleep(1)
        return True

    def rolling_update(self, version: str):
        print(f"[DEPLOY] Starting rolling update to {version}")

        with self.env.lock:
            for i in range(len(self.env.replicas)):
                old = self.env.replicas[i]

                if not old.run_health_check():
                    old.healthy = False

                new_container = Container(version)
                self.env.replicas[i] = new_container

                print(f"[ROLLING UPDATE] Replaced {old.id} -> {new_container.id} ({version})")
                time.sleep(0.5)

        print("[DEPLOY] Update complete with zero downtime")

    def deploy(self, version: str):
        built = self.build(version)
        if self.test(built):
            self.rolling_update(built)


class LoadSimulator:
    def __init__(self, env: Environment):
        self.env = env

    def run(self):
        while True:
            time.sleep(0.3)
            with self.env.lock:
                healthy = [c for c in self.env.replicas if c.run_health_check()]
                if healthy:
                    c = random.choice(healthy)
                    print(f"[TRAFFIC] Routed to {c.id} ({c.version})")
                else:
                    print("[WARNING] No healthy containers available")


def main():
    env = Environment("production", replicas=5)
    pipeline = DeploymentPipeline(env)

    threading.Thread(target=LoadSimulator(env).run, daemon=True).start()

    time.sleep(2)
    pipeline.deploy("v2.0")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()