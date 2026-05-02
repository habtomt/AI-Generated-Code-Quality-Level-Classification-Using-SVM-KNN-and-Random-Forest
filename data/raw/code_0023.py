#!/usr/bin/env python3
"""
dynamic_container_scaler.py
"""

import threading
import time
import random
import uuid
from collections import deque


class Container:
    def __init__(self, name):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.load = 0.0
        self.alive = True

    def simulate_work(self):
        while self.alive:
            self.load = max(0.0, min(1.0, self.load + random.uniform(-0.2, 0.3)))
            time.sleep(1)

    def start(self):
        threading.Thread(target=self.simulate_work, daemon=True).start()


class MetricsStream:
    def __init__(self):
        self.requests = deque(maxlen=50)

    def add_request(self):
        self.requests.append(time.time())

    def get_rps(self):
        now = time.time()
        window = [t for t in self.requests if now - t <= 10]
        return len(window) / 10.0


class Autoscaler:
    def __init__(self, min_replicas=2, max_replicas=10):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.containers = []
        self.metrics = MetricsStream()
        self.lock = threading.Lock()

    def spawn_container(self):
        c = Container("service")
        c.start()
        return c

    def initialize(self):
        for _ in range(self.min_replicas):
            self.containers.append(self.spawn_container())

    def scale(self):
        while True:
            time.sleep(2)
            rps = self.metrics.get_rps()

            with self.lock:
                active = len(self.containers)

                if rps > 5 and active < self.max_replicas:
                    new_c = self.spawn_container()
                    self.containers.append(new_c)
                    print(f"[SCALE UP] RPS={rps:.2f} -> {len(self.containers)} containers")

                elif rps < 2 and active > self.min_replicas:
                    removed = self.containers.pop()
                    removed.alive = False
                    print(f"[SCALE DOWN] RPS={rps:.2f} -> {len(self.containers)} containers")

    def route_request(self):
        while True:
            time.sleep(random.uniform(0.2, 1.0))
            self.metrics.add_request()

            with self.lock:
                if not self.containers:
                    continue
                container = random.choice(self.containers)
                container.load += random.uniform(0.05, 0.2)
                print(f"[REQUEST] routed to {container.id} load={container.load:.2f}")


def main():
    scaler = Autoscaler(min_replicas=3, max_replicas=8)
    scaler.initialize()

    threading.Thread(target=scaler.scale, daemon=True).start()
    threading.Thread(target=scaler.route_request, daemon=True).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()