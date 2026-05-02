#!/usr/bin/env python3

import time
import random
from dataclasses import dataclass, field
from typing import List


@dataclass
class DBInstance:
    id: int
    load: float = 0.0  # 0 to 1 scale

    def update_load(self):
        self.load = random.uniform(0.1, 1.0)


@dataclass
class CloudDBCluster:
    instances: List[DBInstance] = field(default_factory=list)
    max_instances: int = 10
    min_instances: int = 1
    scale_up_threshold: float = 0.75
    scale_down_threshold: float = 0.30

    def average_load(self):
        if not self.instances:
            return 0.0
        return sum(i.load for i in self.instances) / len(self.instances)

    def add_instance(self):
        if len(self.instances) < self.max_instances:
            new_id = len(self.instances) + 1
            self.instances.append(DBInstance(id=new_id))
            print(f"[SCALE UP] Added instance {new_id}")

    def remove_instance(self):
        if len(self.instances) > self.min_instances:
            removed = self.instances.pop()
            print(f"[SCALE DOWN] Removed instance {removed.id}")

    def balance_load(self):
        avg_load = self.average_load()

        if avg_load > self.scale_up_threshold:
            self.add_instance()

        elif avg_load < self.scale_down_threshold:
            self.remove_instance()

    def simulate_load(self):
        for instance in self.instances:
            instance.update_load()

    def status(self):
        loads = ", ".join([f"DB{inst.id}:{inst.load:.2f}" for inst in self.instances])
        print(f"Instances: {len(self.instances)} | Avg Load: {self.average_load():.2f} | {loads}")


def run_simulation():
    cluster = CloudDBCluster(instances=[DBInstance(id=1)])

    for _ in range(20):
        cluster.simulate_load()
        cluster.status()
        cluster.balance_load()
        time.sleep(1)


if __name__ == "__main__":
    run_simulation()