import cv2
import numpy as np
import sys

def apply_image_watermark(frame, watermark, opacity=0.3, position=(20, 20)):
    (h, w) = watermark.shape[:2]
    (x, y) = position

    overlay = frame.copy()

    if y + h > frame.shape[0] or x + w > frame.shape[1]:
        return frame

    roi = overlay[y:y+h, x:x+w]

    blended = cv2.addWeighted(roi, 1 - opacity, watermark, opacity, 0)
    overlay[y:y+h, x:x+w] = blended

    return overlay

def apply_text_watermark(frame, text="WATERMARK", opacity=0.5):
    overlay = frame.copy()
    h, w = frame.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2

    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x = w - text_size[0] - 20
    y = h - 20

    cv2.putText(overlay, text, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    return cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0)

def process_video(input_path, output_path, watermark_path=None, text=None, opacity=0.3):
    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    watermark_img = None
    if watermark_path:
        watermark_img = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
        watermark_img = cv2.resize(watermark_img, (100, 100))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if watermark_img is not None:
            frame = apply_image_watermark(frame, watermark_img, opacity)

        if text:
            frame = apply_text_watermark(frame, text, opacity)

        out.write(frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python watermark.py input.mp4 output.mp4 [watermark.png] [text]")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2]
    watermark_img = sys.argv[3] if len(sys.argv) > 3 else None
    watermark_text = sys.argv[4] if len(sys.argv) > 4 else None

    process_video(input_video, output_video, watermark_img, watermark_text)