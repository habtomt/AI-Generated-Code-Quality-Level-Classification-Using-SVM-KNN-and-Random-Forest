import asyncio
import random
import time
from dataclasses import dataclass

@dataclass
class Event:
    id: int
    timestamp: float
    payload: str

class StreamProcessor:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def produce_events(self):
        event_id = 0
        while True:
            await asyncio.sleep(random.uniform(0.2, 1.0))
            event = Event(
                id=event_id,
                timestamp=time.time(),
                payload=random.choice(["alpha", "beta", "gamma", "delta"])
            )
            await self.queue.put(event)
            event_id += 1

    async def transform_event(self, event: Event) -> Event:
        event.payload = event.payload.upper()
        return event

    async def consume_events(self):
        while True:
            event = await self.queue.get()
            transformed = await self.transform_event(event)
            print(f"Processed Event -> ID: {transformed.id}, Time: {transformed.timestamp}, Payload: {transformed.payload}")
            self.queue.task_done()

    async def run(self):
        producer_task = asyncio.create_task(self.produce_events())
        consumer_task = asyncio.create_task(self.consume_events())

        await asyncio.gather(producer_task, consumer_task)

if __name__ == "__main__":
    processor = StreamProcessor()
    asyncio.run(processor.run())