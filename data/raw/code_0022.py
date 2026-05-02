#!/usr/bin/env python3
"""
redundant_container_orchestrator.py
"""

import random
import threading
import time
import uuid


class ContainerInstance:
    def __init__(self, name):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.alive = True
        self.lock = threading.Lock()

    def run(self):
        while self.alive:
            time.sleep(random.uniform(0.5, 2.0))
            if random.random() < 0.1:
                with self.lock:
                    self.alive = False
                    print(f"[FAIL] Container {self.name}-{self.id} crashed")

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()


class LoadBalancer:
    def __init__(self, containers):
        self.containers = containers
        self.index = 0
        self.lock = threading.Lock()

    def get_next_container(self):
        with self.lock:
            alive_containers = [c for c in self.containers if c.alive]
            if not alive_containers:
                return None
            self.index = (self.index + 1) % len(alive_containers)
            return alive_containers[self.index]


class Orchestrator:
    def __init__(self, app_name, replica_count=3):
        self.app_name = app_name
        self.replica_count = replica_count
        self.containers = []
        self.lock = threading.Lock()

    def deploy(self):
        print(f"[DEPLOY] Starting {self.replica_count} replicas for {self.app_name}")
        for i in range(self.replica_count):
            c = ContainerInstance(f"{self.app_name}-replica-{i}")
            self.containers.append(c)
            c.start()

        threading.Thread(target=self.monitor, daemon=True).start()

    def monitor(self):
        while True:
            time.sleep(2)
            with self.lock:
                for i, c in enumerate(self.containers):
                    if not c.alive:
                        print(f"[RECOVERY] Restarting {c.name}-{c.id}")
                        new_container = ContainerInstance(c.name)
                        self.containers[i] = new_container
                        new_container.start()

    def simulate_requests(self):
        lb = LoadBalancer(self.containers)

        while True:
            time.sleep(1)
            container = lb.get_next_container()
            if container:
                print(f"[REQUEST] Routed to {container.name}-{container.id}")
            else:
                print("[ERROR] No healthy containers available")


def main():
    orchestrator = Orchestrator(app_name="payment-service", replica_count=5)
    orchestrator.deploy()

    orchestrator.simulate_requests()


if __name__ == "__main__":
    main()