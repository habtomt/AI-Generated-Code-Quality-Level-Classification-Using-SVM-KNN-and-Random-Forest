import json
import time
import random
from queue import Queue
from threading import Thread

class IoTStreamProcessor:
    def __init__(self):
        self.stream_buffer = Queue()
        self.storage = []

    def ingest_data(self, device_id):
        while True:
            payload = {
                "timestamp": time.time(),
                "device_id": device_id,
                "temp": random.uniform(20.0, 35.0),
                "status": "active"
            }
            self.stream_buffer.put(json.dumps(payload))
            time.sleep(1)

    def process_and_store(self):
        while True:
            if not self.stream_buffer.empty():
                raw_data = self.stream_buffer.get()
                data = json.loads(raw_data)
                data['processed_at'] = time.time()
                self.storage.append(data)
                if len(self.storage) > 100:
                    self.storage.pop(0)

if __name__ == "__main__":
    processor = IoTStreamProcessor()
    Thread(target=processor.ingest_data, args=("sensor_01",), daemon=True).start()
    Thread(target=processor.process_and_store, daemon=True).start()
    time.sleep(5)