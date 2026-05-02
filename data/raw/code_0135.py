# low_latency_voice_chat.py

import asyncio
import websockets
import numpy as np
import sounddevice as sd
import threading
import queue
import json
from pynput import keyboard

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024

SERVER_URL = "ws://localhost:8765"

audio_queue = queue.Queue()
send_audio = False


# ---------------- NOISE SUPPRESSION (SIMPLE GATE) ---------------- #

def noise_suppress(audio):
    audio = audio.astype(np.float32)
    energy = np.abs(audio).mean()
    if energy < 0.01:
        return np.zeros_like(audio)
    return audio


# ---------------- MICROPHONE STREAM ---------------- #

def audio_callback(indata, frames, time, status):
    if send_audio:
        cleaned = noise_suppress(indata[:, 0])
        audio_queue.put(cleaned.tobytes())


def audio_stream():
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=audio_callback,
        blocksize=CHUNK,
    ):
        while True:
            sd.sleep(100)


# ---------------- KEYBOARD (PUSH TO TALK) ---------------- #

def on_press(key):
    global send_audio
    try:
        if key.char == 't':
            send_audio = True
    except:
        pass


def on_release(key):
    global send_audio
    try:
        if key.char == 't':
            send_audio = False
    except:
        pass


def keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# ---------------- CLIENT ---------------- #

async def sender(ws):
    while True:
        data = await asyncio.get_event_loop().run_in_executor(None, audio_queue.get)
        await ws.send(data)


async def receiver(ws):
    with sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32'
    ) as stream:
        while True:
            msg = await ws.recv()
            audio = np.frombuffer(msg, dtype=np.float32)
            stream.write(audio.reshape(-1, 1))


async def client():
    async with websockets.connect(SERVER_URL) as ws:
        await asyncio.gather(sender(ws), receiver(ws))


# ---------------- SERVER ---------------- #

clients = set()

async def handler(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            for c in clients:
                if c != ws:
                    await c.send(msg)
    finally:
        clients.remove(ws)


async def server():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action="store_true")
    args = parser.parse_args()

    if args.server:
        asyncio.run(server())
    else:
        threading.Thread(target=audio_stream, daemon=True).start()
        threading.Thread(target=keyboard_listener, daemon=True).start()
        asyncio.run(client())