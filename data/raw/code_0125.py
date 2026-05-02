#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys

def convert_video(input_file, output_file, codec, bitrate, resolution, framerate):
    if not os.path.exists(input_file):
        print("Input file does not exist.")
        sys.exit(1)

    command = ["ffmpeg", "-y", "-i", input_file]

    if codec:
        command += ["-c:v", codec]
    if bitrate:
        command += ["-b:v", bitrate]
    if resolution:
        command += ["-s", resolution]
    if framerate:
        command += ["-r", str(framerate)]

    command += ["-c:a", "aac", "-strict", "experimental", output_file]

    try:
        subprocess.run(command, check=True)
        print("Conversion completed successfully.")
    except subprocess.CalledProcessError:
        print("Error occurred during video conversion.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Video format converter using FFmpeg")

    parser.add_argument("input", help="Input video file path")
    parser.add_argument("output", help="Output video file path")
    parser.add_argument("--codec", default="libx264", help="Video codec (default: libx264)")
    parser.add_argument("--bitrate", help="Video bitrate (e.g., 1000k)")
    parser.add_argument("--resolution", help="Output resolution (e.g., 1280x720)")
    parser.add_argument("--framerate", type=int, help="Output frame rate (e.g., 30)")

    args = parser.parse_args()

    convert_video(
        args.input,
        args.output,
        args.codec,
        args.bitrate,
        args.resolution,
        args.framerate
    )


if __name__ == "__main__":
    main()