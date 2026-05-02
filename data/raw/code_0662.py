"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_001.txt
Run      : 1
"""

import os
import subprocess

def convert_video(input_file, output_file, codec='libx264', resolution=None, bitrate=None):
    """
    Convert a video file to a specified format using FFmpeg.
    
    :param input_file: Path to input video file.
    :param output_file: Path where the output video will be saved.
    :param codec: Codec to be used for encoding, default is 'libx264' for MP4 files.
    :param resolution: Desired resolution, e.g., '1280x720', or None to keep original.
    :param bitrate: Desired bitrate, e.g., '500k', or None to use default.
    """
    cmd = ['ffmpeg', '-i', input_file, '-c:v', codec]

    if resolution:
        cmd.extend(['-s', resolution])
        
    if bitrate:
        cmd.extend(['-b:v', bitrate])
    
    cmd.append(output_file)
    
    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: FFmpeg command failed with return code {e.returncode}")
        raise

def main():
    input_file = 'input_video.mp4'  # Specify your input video file path
    output_file = 'output_video.mp4'  # Specify your output video file path

    # Example 1: Convert to MP4 with h.264 codec
    convert_video(input_file, output_file, codec='libx264', resolution='1920x1080', bitrate='500k')
    
    # Example 2: Convert to AVI with xvid codec
    # convert_video(input_file, 'output_video.avi', codec='xvid', resolution='640x480', bitrate='1000k')
    
    # Example 3: Convert to WebM with VP9 codec
    # convert_video(input_file, 'output_video.webm', codec='libvpx', resolution='1280x720', bitrate='500k')

if __name__ == '__main__':
    main()