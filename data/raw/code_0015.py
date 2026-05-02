#!/usr/bin/env python3

import time
import random
import logging
from dataclasses import dataclass, field

try:
    import psutil
except ImportError:
    psutil = None


logging.basicConfig(
    filename="db_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------
# METRICS SIMULATION / COLLECTION
# ---------------------------

@dataclass
class DBMetrics:
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    query_latency_ms: float = 0.0
    storage_usage_gb: float = 0.0


class MetricsCollector:
    def __init__(self):
        self.storage = 50.0  # simulated GB used

    def collect_system_metrics(self):
        if psutil:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
        else:
            cpu = random.uniform(10, 90)
            mem = random.uniform(20, 85)

        query_latency = random.uniform(10, 300)
        self.storage += random.uniform(0.01, 0.2)

        return DBMetrics(
            cpu_usage=cpu,
            memory_usage=mem,
            query_latency_ms=query_latency,
            storage_usage_gb=self.storage
        )


# ---------------------------
# ANALYSIS ENGINE
# ---------------------------

class Analyzer:
    def __init__(self):
        self.cpu_threshold = 80
        self.mem_threshold = 80
        self.latency_threshold = 200
        self.storage_threshold = 80

    def analyze(self, metrics: DBMetrics):
        alerts = []
        suggestions = []

        if metrics.cpu_usage > self.cpu_threshold:
            alerts.append("High CPU usage detected")
            suggestions.append("Scale up compute instances or optimize queries")

        if metrics.memory_usage > self.mem_threshold:
            alerts.append("High memory usage detected")
            suggestions.append("Enable caching or increase memory allocation")

        if metrics.query_latency_ms > self.latency_threshold:
            alerts.append("Slow query performance detected")
            suggestions.append("Optimize indexes or query plans")

        if metrics.storage_usage_gb > self.storage_threshold:
            alerts.append("High storage usage detected")
            suggestions.append("Archive old data or increase storage capacity")

        return alerts, suggestions


# ---------------------------
# ALERTING SYSTEM
# ---------------------------

class AlertSystem:
    def send_alert(self, alerts, suggestions):
        for alert in alerts:
            logging.warning(alert)
            print(f"[ALERT] {alert}")

        for suggestion in suggestions:
            logging.info(suggestion)
            print(f"[SUGGESTION] {suggestion}")


# ---------------------------
# MONITORING LOOP
# ---------------------------

class CloudDBMonitor:
    def __init__(self):
        self.collector = MetricsCollector()
        self.analyzer = Analyzer()
        self.alert_system = AlertSystem()

    def run(self):
        print("Starting cloud database monitoring...")

        while True:
            metrics = self.collector.collect_system_metrics()

            print("\n--- METRICS ---")
            print(f"CPU: {metrics.cpu_usage:.2f}%")
            print(f"Memory: {metrics.memory_usage:.2f}%")
            print(f"Query Latency: {metrics.query_latency_ms:.2f} ms")
            print(f"Storage: {metrics.storage_usage_gb:.2f} GB")

            alerts, suggestions = self.analyzer.analyze(metrics)

            if alerts:
                self.alert_system.send_alert(alerts, suggestions)
            else:
                print("[OK] All systems normal")

            time.sleep(2)


# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":
    monitor = CloudDBMonitor()
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")