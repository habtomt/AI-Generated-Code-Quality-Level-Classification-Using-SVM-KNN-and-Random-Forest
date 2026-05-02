"""
Auto-generated Python code
Scenario : Video Processing
Prompt   : response_002.txt
Run      : 1
"""

import cv2
import numpy as np

# Read input video
cap = cv2.VideoCapture('input.mp4')

# Get frame count, width, and height
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Set up output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

# Read the first frame
_, prev = cap.read() 
prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

# Pre-define transformation-store array
transforms = np.zeros((n_frames-1, 3), np.float32) 

for i in range(n_frames-1):
    try:
        # Detect feature points in previous frame
        prev_pts = cv2.goodFeaturesToTrack(prev_gray, 
                                           maxCorners=200, 
                                           qualityLevel=0.01, 
                                           minDistance=30, 
                                           blockSize=3)

        # Read next frame
        success, curr = cap.read()
        if not success: 
            break

        # Convert to grayscale
        curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow (i.e. track feature points)
        curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)

        # Sanity check
        assert prev_pts.shape == curr_pts.shape 

        # Filter only valid points
        idx = np.where(status==1)[0]
        prev_pts = prev_pts[idx]
        curr_pts = curr_pts[idx]

        # Find transformation matrix
        m, _ = cv2.estimateAffine2D(prev_pts, curr_pts) # Will only work with OpenCV 3 or 4

        # Extract translation
        dx = m[0,2]
        dy = m[1,2]
        
        # Extract rotation angle
        da = np.arctan2(m[1,0], m[0,0])

        # Store transformation
        transforms[i] = [dx,dy,da]

        # Move to next frame
        prev_gray = curr_gray

    except Exception as e:
        print(f"Error occurred: {e}")
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        break

# Compute trajectory using cumulative sum of transformations
trajectory = np.cumsum(transforms, axis=0)

# Create variable to store smoothed trajectory
smoothed_trajectory = np.copy(trajectory)

# Filter the trajectory
SMOOTHING_RADIUS = 30 
for i in range(3):
    smoothed_trajectory[:,i] = np.convolve(trajectory[:,i], np.ones((SMOOTHING_RADIUS,))/SMOOTHING_RADIUS, mode='same')

# Calculate difference in smoothed_trajectory and trajectory
difference = smoothed_trajectory - trajectory

# Calculate newer transformation array
transforms_smooth = transforms + difference

# Reset stream to first frame
cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 

for i in range(n_frames-1):
    try:
        # Read next frame
        success, frame = cap.read()
        if not success:
            break

        # Extract transformations from the new transformation array
        dx = transforms_smooth[i,0]
        dy = transforms_smooth[i,1]
        da = transforms_smooth[i,2]

        # Reconstruct transformation matrix accordingly to new values
        m = np.zeros((2,3), np.float32)
        m[0,0] = np.cos(da)
        m[0,1] = -np.sin(da)
        m[1,0] = np.sin(da)
        m[1,1] = np.cos(da)
        m[0,2] = dx
        m[1,2] = dy

        # Apply affine wrapping to the given frame
        frame_stabilized = cv2.warpAffine(frame, m, (width, height))

        # Fix border artifacts
        frame_stabilized = cv2.copyMakeBorder(frame_stabilized, 10, 10, 10, 10, cv2.BORDER_REPLICATE)

        # Write the frame to the file
        frame_out = cv2.hconcat([frame, frame_stabilized])

        # If the frame_out is not larger than width, treat the frame differently
        if frame_out.shape[1] > 1920:
            frame_out = cv2.resize(frame_out, (1920, int(frame_out.shape[0] * 1920 / frame_out.shape[1])))

        out.write(frame_out)

    except Exception as e:
        print(f"Error occurred: {e}")
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        break

# Release the video reader and writer
cap.release()
out.release()

# Close all windows
cv2.destroyAllWindows()