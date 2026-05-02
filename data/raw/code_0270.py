import subprocess
import os

def reduce_video_size(input_file, output_file, target_resolution="1280x720", bitrate="1M", codec="libx264"):
    """
    Reduces video file size using FFmpeg.
    
    Parameters:
    - input_file: Path to the source video.
    - output_file: Path to save the compressed video.
    - target_resolution: New resolution (e.g., '1920x1080', '1280x720', '640x360').
    - bitrate: Target video bitrate (e.g., '1M' for 1Mbps, '500k' for 500kbps).
    - codec: Video codec to use (h264 is standard for compatibility/compression).
    """
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    # FFmpeg command construction
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vcodec', codec,
        '-s', target_resolution,
        '-b:v', bitrate,
        '-preset', 'medium',
        '-acodec', 'aac',
        '-strict', 'experimental',
        output_file
    ]

    try:
        print(f"Starting compression: {input_file} -> {output_file}")
        subprocess.run(command, check=True)
        print("Compression complete!")
        
        initial_size = os.path.getsize(input_file) / (1024 * 1024)
        final_size = os.path.getsize(output_file) / (1024 * 1024)
        
        print(f"Initial Size: {initial_size:.2f} MB")
        print(f"Reduced Size: {final_size:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during processing: {e}")
    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not in your PATH.")

if __name__ == "__main__":
    # Example usage
    input_video = "input_video.mp4" 
    output_video = "compressed_video.mp4"
    
    reduce_video_size(input_video, output_video, target_resolution="1280x720", bitrate="1M")