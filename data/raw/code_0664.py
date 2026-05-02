"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_003.txt
Run      : 1
"""

import cv2
import numpy as np

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    # Brightness and contrast adjustment
    brightness = int((brightness - 0.5) * 255)
    contrast = int((contrast - 0.5) * 255)
    
    # Apply contrast
    adjusted = cv2.convertScaleAbs(image, alpha=1 + contrast / 127.0, beta=brightness)
    return adjusted

def enhance_video(input_path, output_path):
    # Capture the input video
    cap = cv2.VideoCapture(input_path)

    # Get frame count, height, width, and frames per second
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Enhance video frame
        
        # Convert to Lab color space for better color correction
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        # Split channels
        l, a, b = cv2.split(lab)
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L-channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        lab = cv2.merge((cl, a, b))
        # Convert back to BGR
        frame_clahe = cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)
        
        # Apply brightness and contrast adjustment
        frame_adj = adjust_brightness_contrast(frame_clahe, brightness=0.5, contrast=0.5)
        
        # Apply sharpening
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        frame_sharp = cv2.filter2D(frame_adj, -1, kernel)

        # Write the frame to the output video
        out.write(frame_sharp)

    # Release everything if job is finished
    cap.release()
    out.release()

# Example usage
input_video_path = 'input_video.mp4'
output_video_path = 'enhanced_video.mp4'

enhance_video(input_video_path, output_video_path)