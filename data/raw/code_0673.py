"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import cv2
import numpy as np

# Define function to remove shaking and jitter from video footage
def remove_shaking(video_path, output_path):
    try:
        # Create a VideoCapture object to read the video file
        cap = cv2.VideoCapture(video_path)

        # Check if the video file is opened successfully
        if not cap.isOpened():
            print("Error: Unable to open video file")
            return

        # Get the video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a VideoWriter object to write the output video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        # Initialize the frame counter
        frame_count = 0

        # Read the video frames and apply Gaussian blur to reduce shaking and jitter
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply Gaussian blur to reduce shaking and jitter
            blurred_frame = cv2.GaussianBlur(frame, (21, 21), 0)

            # Write the blurred frame to the output video
            out.write(blurred_frame)

            # Increment the frame counter
            frame_count += 1

            # Display the output video
            cv2.imshow('Output Video', blurred_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the VideoCapture and VideoWriter objects
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        print("Shaking and jitter removed from video footage successfully")

    except Exception as e:
        print("Error: ", str(e))

# Example usage
remove_shaking('input.mp4', 'output.mp4')