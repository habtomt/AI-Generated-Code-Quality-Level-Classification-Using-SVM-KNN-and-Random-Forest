import subprocess
import os

def convert_video(input_file, output_file, video_codec="libx264", audio_codec="aac", bitrate="2M", fps=30):
    """
    Converts video files between formats with specified encoding settings.
    Common formats: .mp4, .mkv, .mov, .avi
    """
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # FFmpeg command for format conversion and encoding adjustment
    command = [
        'ffmpeg',
        '-i', input_file,        # Input file
        '-vcodec', video_codec,   # Video codec (e.g., libx264, libx265, vp9)
        '-acodec', audio_codec,   # Audio codec (e.g., aac, mp3)
        '-b:v', bitrate,          # Video bitrate
        '-r', str(fps),           # Frames per second
        '-pix_fmt', 'yuv420p',    # Ensures compatibility with most players
        '-y',                     # Overwrite output file if exists
        output_file
    ]

    try:
        print(f"Converting: {input_file} -> {output_file}...")
        subprocess.run(command, check=True, capture_output=True)
        print(f"Success! File saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e.stderr.decode()}")
    except FileNotFoundError:
        print("Error: FFmpeg not found. Please install FFmpeg to use this script.")

if __name__ == "__main__":
    # Conversion Examples
    
    # 1. Convert MKV to MP4 (High Compatibility)
    convert_video(
        input_file="source_video.mkv", 
        output_file="output_compat.mp4", 
        video_codec="libx264", 
        bitrate="4M"
    )

    # 2. Convert MP4 to WebM (For Web usage)
    convert_video(
        input_file="source_video.mp4", 
        output_file="output_web.webm", 
        video_codec="libvpx-vp9", 
        audio_codec="libopus",
        bitrate="1M"
    )