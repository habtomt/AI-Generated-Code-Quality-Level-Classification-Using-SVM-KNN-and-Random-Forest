import cv2
import numpy as np
import sys

def adjust_brightness_contrast(frame, brightness=30, contrast=1.2):
    return cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

def sharpen_frame(frame):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)

def color_correction(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    s = cv2.add(s, 15)
    v = cv2.add(v, 10)

    hsv = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def enhance_frame(frame):
    frame = color_correction(frame)
    frame = adjust_brightness_contrast(frame)
    frame = sharpen_frame(frame)
    return frame

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        enhanced = enhance_frame(frame)
        out.write(enhanced)

    cap.release()
    out.release()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python enhancer.py input.mp4 output.mp4")
        sys.exit(1)

    process_video(sys.argv[1], sys.argv[2])