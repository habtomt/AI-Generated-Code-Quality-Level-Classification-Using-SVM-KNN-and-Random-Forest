# virtual_customer_support.py

import asyncio
import websockets
import threading
import sounddevice as sd
import numpy as np
import wave
import time
import json
from collections import defaultdict

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024

rooms = defaultdict(set)
recordings = defaultdict(list)
analytics = defaultdict(lambda: {"volume": [], "duration": 0})


# ---------------- AUDIO UTIL ---------------- #

def rms(audio):
    return float(np.sqrt(np.mean(np.square(audio)))) if len(audio) else 0.0


# ---------------- SERVER ---------------- #

async def handler(ws):
    params = await ws.recv()
    info = json.loads(params)

    room = info["room"]
    role = info.get("role", "customer")

    rooms[room].add(ws)
    start_time = time.time()

    try:
        async for msg in ws:
            data = np.frombuffer(msg, dtype=np.float32)

            analytics[room]["volume"].append(rms(data))

            recordings[room].append(data.tobytes())

            for client in rooms[room]:
                if client != ws:
                    await client.send(msg)

    finally:
        rooms[room].remove(ws)
        analytics[room]["duration"] += time.time() - start_time

        save_recording(room)
        print(f"Room {room} closed. Analytics:", analytics[room])


def save_recording(room):
    if room not in recordings:
        return

    audio_bytes = b"".join(recordings[room])
    audio = np.frombuffer(audio_bytes, dtype=np.float32)

    filename = f"{room}_call.wav"

    audio_int16 = np.int16(audio * 32767)

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())

    print(f"Saved recording: {filename}")


async def server():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()


# ---------------- CLIENT ---------------- #

audio_queue = asyncio.Queue()
send_audio = True


def audio_callback(indata, frames, time_info, status):
    if send_audio:
        audio_queue.put_nowait(indata[:, 0].astype(np.float32).tobytes())


def audio_input():
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=audio_callback,
        blocksize=CHUNK,
    ):
        while True:
            sd.sleep(100)


def audio_output(stream, data):
    audio = np.frombuffer(data, dtype=np.float32)
    stream.write(audio.reshape(-1, 1))


async def sender(ws):
    while True:
        data = await audio_queue.get()
        await ws.send(data)


async def receiver(ws):
    with sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    ) as stream:
        while True:
            msg = await ws.recv()
            audio_output(stream, msg)


async def client():
    room = input("Enter room id: ")
    role = input("Enter role (agent/customer): ")

    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send(json.dumps({"room": room, "role": role}))

        await asyncio.gather(sender(ws), receiver(ws))


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action="store_true")
    args = parser.parse_args()

    if args.server:
        asyncio.run(server())
    else:
        threading.Thread(target=audio_input, daemon=True).start()
        asyncio.run(client())