"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2

def add_watermark(video_path, output_path, watermark_path, watermark_opacity=0.5):
    """
    Add a transparent or opaque watermark to a video.

    Args:
    - video_path (str): Path to the input video file.
    - output_path (str): Path to the output video file.
    - watermark_path (str): Path to the watermark image file.
    - watermark_opacity (float, optional): Opacity of the watermark (0.0 to 1.0). Defaults to 0.5.

    Returns:
    - None
    """

    try:
        # Read the watermark image
        watermark = cv2.imread(watermark_path)

        # Create a video capture object
        cap = cv2.VideoCapture(video_path)

        # Get the video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Read frames from the video
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Add the watermark to the frame
            frame_with_watermark = add_watermark_to_frame(frame_rgb, watermark, watermark_opacity)

            # Convert the frame back to BGR
            frame_with_watermark_bgr = cv2.cvtColor(frame_with_watermark, cv2.COLOR_RGB2BGR)

            # Write the frame with the watermark to the output video
            out.write(frame_with_watermark_bgr)

        # Release the video capture and writer objects
        cap.release()
        out.release()

    except Exception as e:
        print(f"An error occurred: {e}")


def add_watermark_to_frame(frame, watermark, opacity):
    """
    Add a transparent or opaque watermark to a frame.

    Args:
    - frame (numpy array): Input frame.
    - watermark (numpy array): Watermark image.
    - opacity (float): Opacity of the watermark (0.0 to 1.0).

    Returns:
    - numpy array: Frame with the watermark.
    """

    try:
        # Get the shapes of the frame and the watermark
        frame_h, frame_w, _ = frame.shape
        watermark_h, watermark_w, _ = watermark.shape

        # Calculate the position of the watermark in the frame
        x = (frame_w - watermark_w) // 2
        y = (frame_h - watermark_h) // 2

        # Create a new frame with the watermark
        frame_with_watermark = np.copy(frame)

        # Add the watermark to the frame with the given opacity
        for i in range(watermark_h):
            for j in range(watermark_w):
                if watermark[i, j, 3] > 0:
                    for k in range(3):
                        frame_with_watermark[y + i, x + j, k] = (1 - opacity) * frame_with_watermark[y + i, x + j, k] + opacity * watermark[i, j, k]

        return frame_with_watermark

    except Exception as e:
        print(f"An error occurred: {e}")
        return frame


# Example usage
video_path = "input.mp4"
output_path = "output.mp4"
watermark_path = "watermark.png"

add_watermark(video_path, output_path, watermark_path)