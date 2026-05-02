# realtime_video_conference.py

import asyncio
import json
import argparse
import cv2
import numpy as np
from aiohttp import web
import aiohttp
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay

pcs = set()

# ---------------- SIGNALING SERVER ---------------- #

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.Response(text="WebRTC Signaling Server Running")

@routes.post("/offer")
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    relay = MediaRelay()
    player = MediaPlayer("/dev/video0" if not args.screen else "desktop", format="v4l2" if not args.screen else None)

    if player.video:
        pc.addTrack(relay.subscribe(player.video))

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            print("Chat:", message)
            channel.send(f"echo: {message}")

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )


def run_server():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8080)


# ---------------- CLIENT ---------------- #

class DummyVideo(VideoStreamTrack):
    def __init__(self):
        super().__init__()

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        frame = np.zeros((480, 640, 3), np.uint8)
        cv2.putText(frame, "SCREEN SHARE / VIDEO", (50, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return VideoFrame.from_ndarray(frame, format="bgr24")


async def run_client():
    pc = RTCPeerConnection()

    channel = pc.createDataChannel("chat")

    @channel.on("open")
    def on_open():
        asyncio.create_task(chat_loop(channel))

    @channel.on("message")
    def on_message(message):
        print("Peer:", message)

    player = MediaPlayer("/dev/video0")
    if player.video:
        pc.addTrack(player.video)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8080/offer", json={
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }) as resp:
            data = await resp.json()

    await pc.setRemoteDescription(
        RTCSessionDescription(sdp=data["sdp"], type=data["type"])
    )

    await asyncio.Future()


async def chat_loop(channel):
    while True:
        msg = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")
        channel.send(msg)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action="store_true")
    parser.add_argument("--screen", action="store_true")
    args = parser.parse_args()

    if args.server:
        run_server()
    else:
        asyncio.run(run_client())