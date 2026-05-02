"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_000.txt
Run      : 1
"""

import subprocess

def reduce_video_size(input_file, output_file, target_bitrate=None, resolution=None, codec='libx264'):
    """
    Reduce the size of a video file while maintaining acceptable quality.
    
    Parameters:
    - input_file: str, the path to the input video file.
    - output_file: str, the path to the output compressed video file.
    - target_bitrate: str, desired output bitrate (e.g., '500k' for 500 kbps). Optional.
    - resolution: str, desired output resolution (e.g., '1280x720'). Optional.
    - codec: str, video codec to use (e.g., 'libx265' for better compression/quality ratio). Default is 'libx264'.
    """
    # Construct the ffmpeg command
    command = ['ffmpeg', '-i', input_file, '-c:v', codec]
    
    # Adjust the video bitrate if specified
    if target_bitrate:
        command.extend(['-b:v', target_bitrate])
    
    # Adjust the resolution if specified
    if resolution:
        command.extend(['-vf', f'scale={resolution}'])
    
    # Add the output file to the command
    command.append(output_file)
    
    # Execute the ffmpeg command
    try:
        subprocess.run(command, check=True)
        print(f"Video file compressed and saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while processing the video: {e}")

# Example usage
input_video_path = "YOUR_INPUT_VIDEO_PATH.mp4"
output_video_path = "compressed_video.mp4"
reduce_video_size(input_video_path, output_video_path, target_bitrate='500k', resolution='1280x720', codec='libx265')