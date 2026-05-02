#!/usr/bin/env python3
import subprocess
import threading
import time
import argparse
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class StreamConfig:
    name: str
    input_source: str  # e.g. webcam or video file
    rtmp_url: str
    resolution: str = "1280x720"
    bitrate: str = "2500k"
    fps: int = 30


class AdaptiveStreamer:
    def __init__(self, config: StreamConfig):
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.running = False

    def build_ffmpeg_cmd(self):
        width, height = self.config.resolution.split("x")

        cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1",
            "-i", self.config.input_source,
            "-vf", f"scale={width}:{height}",
            "-r", str(self.config.fps),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-b:v", self.config.bitrate,
            "-maxrate", self.config.bitrate,
            "-bufsize", str(int(self.config.bitrate.replace('k','')) * 2) + "k",
            "-pix_fmt", "yuv420p",
            "-f", "flv",
            self.config.rtmp_url
        ]
        return cmd

    def start(self):
        self.running = True
        while self.running:
            cmd = self.build_ffmpeg_cmd()
            print(f"[{self.config.name}] Starting stream: {' '.join(cmd)}")

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.process.wait()

            if self.running:
                print(f"[{self.config.name}] Stream crashed. Restarting in 3 seconds...")
                time.sleep(3)

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
            self.process = None


class StreamManager:
    def __init__(self):
        self.streams: List[AdaptiveStreamer] = []
        self.threads: List[threading.Thread] = []

    def add_stream(self, config: StreamConfig):
        streamer = AdaptiveStreamer(config)
        self.streams.append(streamer)

    def start_all(self):
        for streamer in self.streams:
            t = threading.Thread(target=streamer.start, daemon=True)
            self.threads.append(t)
            t.start()

    def stop_all(self):
        for streamer in self.streams:
            streamer.stop()


def adaptive_resolution_controller(manager: StreamManager):
    """
    Simulated adaptive logic:
    changes resolution every 20 seconds for demo purposes.
    """
    resolutions = ["1920x1080", "1280x720", "854x480"]

    idx = 0
    while True:
        time.sleep(20)
        idx = (idx + 1) % len(resolutions)

        print(f"[Adaptive] Switching all streams to {resolutions[idx]}")

        for streamer in manager.streams:
            streamer.stop()
            streamer.config.resolution = resolutions[idx]

        manager.start_all()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Video input source (file or webcam)")
    parser.add_argument("--rtmp", required=True, help="Base RTMP URL (e.g. rtmp://localhost/live/stream)")
    args = parser.parse_args()

    manager = StreamManager()

    # Multiple concurrent streams (simulated multi-channel broadcast)
    manager.add_stream(StreamConfig(
        name="stream_1",
        input_source=args.input,
        rtmp_url=args.rtmp + "_1",
        resolution="1280x720",
        bitrate="2500k"
    ))

    manager.add_stream(StreamConfig(
        name="stream_2",
        input_source=args.input,
        rtmp_url=args.rtmp + "_2",
        resolution="854x480",
        bitrate="1200k"
    ))

    manager.add_stream(StreamConfig(
        name="stream_3",
        input_source=args.input,
        rtmp_url=args.rtmp + "_3",
        resolution="1920x1080",
        bitrate="4000k"
    ))

    manager.start_all()

    controller_thread = threading.Thread(
        target=adaptive_resolution_controller,
        args=(manager,),
        daemon=True
    )
    controller_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping streams...")
        manager.stop_all()


if __name__ == "__main__":
    main()