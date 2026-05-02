import threading
import queue
import time
import random
import json
import sqlite3
from datetime import datetime

# Thread-safe queue for streaming IoT data
data_queue = queue.Queue()

# SQLite database setup
conn = sqlite3.connect("iot_stream.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL,
    pressure REAL
)
""")
conn.commit()

# Simulated IoT device producer
class IoTDevice(threading.Thread):
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.running = True

    def generate_data(self):
        return {
            "device_id": self.device_id,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(random.uniform(15, 35), 2),
            "humidity": round(random.uniform(30, 90), 2),
            "pressure": round(random.uniform(950, 1050), 2),
        }

    def run(self):
        while self.running:
            data = self.generate_data()
            data_queue.put(data)
            time.sleep(random.uniform(0.5, 2))

    def stop(self):
        self.running = False


# Consumer that processes and stores data
class DataProcessor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True

    def store_data(self, data):
        cursor.execute("""
        INSERT INTO sensor_data (device_id, timestamp, temperature, humidity, pressure)
        VALUES (?, ?, ?, ?, ?)
        """, (
            data["device_id"],
            data["timestamp"],
            data["temperature"],
            data["humidity"],
            data["pressure"]
        ))
        conn.commit()

    def run(self):
        while self.running:
            try:
                data = data_queue.get(timeout=1)
                self.store_data(data)
                print(f"Stored: {data}")
            except queue.Empty:
                continue

    def stop(self):
        self.running = False


def main():
    devices = [IoTDevice(f"device_{i}") for i in range(3)]
    processor = DataProcessor()

    for d in devices:
        d.start()

    processor.start()

    try:
        time.sleep(20)
    except KeyboardInterrupt:
        pass
    finally:
        for d in devices:
            d.stop()
        processor.stop()

        for d in devices:
            d.join()
        processor.join()

        conn.close()


if __name__ == "__main__":
    main()