"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_002.txt
Run      : 2
"""

import cv2
import numpy as np
from moviepy.editor import VideoFileClip

# Define the function to stabilize video
def stabilize_video(video_path, output_path):
    try:
        # Read the video
        video = VideoFileClip(video_path)
        
        # Define the frame rate and the number of frames to skip
        fps = video.fps
        skip_frames = int(fps / 2)
        
        # Convert the video to grayscale
        gray = video.fl_image(lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        
        # Create a Lucas-Kanade optical flow tracker
        lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # Initialize the points to track
        prev_gray = None
        pts = None
        
        # Create a list to store the frames
        frames = []
        
        # Iterate over the frames
        for frame in video.iter_frames(progress_bar=True):
            if prev_gray is not None:
                # Convert the frame to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Calculate the optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray_frame, pts, None, **lk_params)
                
                # Get the good points
                good_new = p1[st==1]
                good_old = pts[st==1]
                
                # Convert the points to floats
                good_new = good_new.astype(np.float32)
                good_old = good_old.astype(np.float32)
                
                # Calculate the homography matrix
                homography, _ = cv2.findHomography(good_old, good_new, cv2.RANSAC, 5.0)
                
                # Warp the frame using the homography matrix
                warped_frame = cv2.warpPerspective(frame, homography, (frame.shape[1], frame.shape[0]))
                
                # Append the warped frame to the list
                frames.append(warped_frame)
            
            # Update the previous frame and points
            prev_gray = gray_frame
            pts = good_new
            
            # Increment the frame counter
            skip_frames = (skip_frames - 1) % len(frames)
        
        # Create a new video from the stabilized frames
        stabilized_video = VideoFileClip(frames, fps=fps).set_duration(video.duration)
        
        # Write the stabilized video to file
        stabilized_video.write_videofile(output_path)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Set the input and output video paths
input_path = "input.mp4"
output_path = "output.mp4"

# Call the function to stabilize the video
stabilize_video(input_path, output_path)