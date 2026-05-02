"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_004.txt
Run      : 3
"""

from moviepy.editor import *
from moviepy.video.fx import resize
from PIL import Image

def add_watermark(video_file, watermark_image, output_file, opacity=0.5):
    """
    Adds a transparent or opaque watermark to a video.

    Args:
        video_file (str): Path to the input video file.
        watermark_image (str): Path to the watermark image file.
        output_file (str): Path to the output video file.
        opacity (float): Opacity of the watermark (0.0 - 1.0).
    """
    try:
        # Load the video
        video = VideoFileClip(video_file)

        # Load the watermark image
        img = Image.open(watermark_image)

        # Resize the watermark image to fit the video
        resized_img = resize(img, width=(video.w // 10))

        # Create a transparent overlay
        overlay = ColorClip(resized_img.shape, color=(0, 0, 0, 1 - opacity))

        # Add the overlay to the video
        video_with_watermark = CompositeVideoClip([video.set_position('center'), overlay.set_position((0.5, 0.5))])

        # Write the video to the output file
        video_with_watermark.write_videofile(output_file)

    except Exception as e:
        print(f"Error adding watermark: {e}")

# Example usage:
add_watermark("input.mp4", "watermark.png", "output.mp4", opacity=0.5)