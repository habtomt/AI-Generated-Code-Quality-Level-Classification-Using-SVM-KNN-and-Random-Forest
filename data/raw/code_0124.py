#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys


def run_ffmpeg(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e}")
        sys.exit(1)


def compress_video(input_path, output_path, resolution=None, bitrate=None, codec="libx264"):
    cmd = ["ffmpeg", "-i", input_path]

    if resolution:
        cmd += ["-vf", f"scale={resolution}"]

    if bitrate:
        cmd += ["-b:v", bitrate]

    cmd += ["-c:v", codec, "-preset", "medium", "-crf", "23", "-c:a", "aac", "-b:a", "128k", output_path]

    run_ffmpeg(cmd)


def get_file_size(path):
    return os.path.getsize(path) / (1024 * 1024)


def main():
    parser = argparse.ArgumentParser(description="Video compression tool")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--resolution", help="Set resolution e.g. 1280:720", default=None)
    parser.add_argument("--bitrate", help="Set video bitrate e.g. 800k", default=None)
    parser.add_argument("--codec", help="Video codec (default libx264)", default="libx264")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("Input file does not exist")
        sys.exit(1)

    print(f"Original size: {get_file_size(args.input):.2f} MB")

    compress_video(args.input, args.output, args.resolution, args.bitrate, args.codec)

    print(f"Compressed size: {get_file_size(args.output):.2f} MB")
    print("Done.")


if __name__ == "__main__":
    main()