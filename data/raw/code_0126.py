import cv2
import numpy as np
import sys

def moving_average(curve, radius):
    window_size = 2 * radius + 1
    filter_kernel = np.ones(window_size) / window_size
    curve_pad = np.pad(curve, (radius, radius), mode='edge')
    smoothed = np.convolve(curve_pad, filter_kernel, mode='same')
    return smoothed[radius:-radius]

def smooth_trajectory(trajectory, radius=5):
    smoothed = np.copy(trajectory)
    for i in range(3):
        smoothed[:, i] = moving_average(trajectory[:, i], radius)
    return smoothed

def fix_border(frame):
    h, w = frame.shape[:2]
    T = cv2.getRotationMatrix2D((w / 2, h / 2), 0, 1.04)
    return cv2.warpAffine(frame, T, (w, h))

def stabilize_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    _, prev = cap.read()
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    transforms = np.zeros((n_frames - 1, 3))

    for i in range(n_frames - 1):
        ret, curr = cap.read()
        if not ret:
            break

        curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

        prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)
        curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)

        idx = np.where(status == 1)[0]
        prev_pts = prev_pts[idx]
        curr_pts = curr_pts[idx]

        m, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)

        dx = m[0, 2]
        dy = m[1, 2]
        da = np.arctan2(m[1, 0], m[0, 0])

        transforms[i] = [dx, dy, da]

        prev_gray = curr_gray

    trajectory = np.cumsum(transforms, axis=0)
    smooth = smooth_trajectory(trajectory)

    diff = smooth - trajectory
    transforms_smooth = transforms + diff

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    for i in range(n_frames - 1):
        ret, frame = cap.read()
        if not ret:
            break

        dx = transforms_smooth[i, 0]
        dy = transforms_smooth[i, 1]
        da = transforms_smooth[i, 2]

        m = np.zeros((2, 3))
        m[0, 0] = np.cos(da)
        m[0, 1] = -np.sin(da)
        m[1, 0] = np.sin(da)
        m[1, 1] = np.cos(da)
        m[0, 2] = dx
        m[1, 2] = dy

        stabilized = cv2.warpAffine(frame, m, (w, h))
        stabilized = fix_border(stabilized)

        out.write(stabilized)

    cap.release()
    out.release()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python stabilizer.py input.mp4 output.mp4")
        sys.exit(1)

    stabilize_video(sys.argv[1], sys.argv[2])