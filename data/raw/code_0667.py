"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_001.txt
Run      : 2
"""

import os
from moviepy.editor import *
import ffmpeg

# Define a function to convert video files
def convert_video(input_file, output_file, input_format, output_format, resolution=(1920, 1080), fps=30):
    try:
        # Open the input video file
        video = VideoFileClip(input_file)

        # Set the resolution and frame rate
        video = video.resize(resolution)
        video = video.set_fps(fps)

        # Set the output video file path
        output_path = os.path.splitext(output_file)[0]
        output_path += f".{output_format}"

        # Write the output video file
        video.write_videofile(output_path, codec=output_format)

        print(f"Video converted successfully: {output_path}")

    except Exception as e:
        print(f"Error converting video: {e}")


# Define a function to convert video files using FFmpeg
def convert_video_ffmpeg(input_file, output_file, resolution=(1920, 1080), fps=30):
    try:
        # Set the input and output file paths
        input_path = input_file
        output_path = output_file

        # Set the resolution and frame rate
        width = resolution[0]
        height = resolution[1]
        framerate = fps

        # Create the FFmpeg command
        command = f"ffmpeg -i {input_path} -vf scale={width}:{height} -r {framerate} -c:v libx264 -crf 18 {output_path}"

        # Execute the FFmpeg command
        os.system(command)

        print(f"Video converted successfully: {output_path}")

    except Exception as e:
        print(f"Error converting video: {e}")


# Example usage
if __name__ == "__main__":
    input_file = "input.mp4"  # Replace with your input video file
    output_file = "output.mp4"  # Replace with your desired output file

    # Convert video using MoviePy
    convert_video(input_file, output_file, "mp4", "mp4")

    # Convert video using FFmpeg
    convert_video_ffmpeg(input_file, output_file)