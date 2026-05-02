"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_000.txt
Run      : 2
"""

import os
from moviepy.editor import *
from PIL import Image

def reduce_video_size(input_file, output_file, bitrate='30M', resolution=None, codec='libx264'):
    """
    Reduces video file size while maintaining acceptable quality.

    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to the output video file.
        bitrate (str, optional): Bitrate for the output video. Defaults to '30M'.
        resolution (tuple, optional): Resolution for the output video. Defaults to None.
        codec (str, optional): Codec for the output video. Defaults to 'libx264'.
    """

    # Load the video file using MoviePy
    video = VideoFileClip(input_file)

    # Adjust the bitrate
    video = video.vset_bitrate(bitrate)

    # Adjust the resolution
    if resolution:
        # Resize the video using PIL
        image = Image.new('RGB', (resolution[0], resolution[1]))
        image.save('temp.jpg')
        video = video.set_resolution(resolution)

    # Adjust the codec
    video = video.set_vcodec(codec)

    # Write the output video
    video.write_videofile(output_file)

    # Remove the temporary image file
    os.remove('temp.jpg')

# Example usage
input_file = 'input.mp4'
output_file = 'output.mp4'
reduce_video_size(input_file, output_file, bitrate='10M', resolution=(1280, 720), codec='libx264')