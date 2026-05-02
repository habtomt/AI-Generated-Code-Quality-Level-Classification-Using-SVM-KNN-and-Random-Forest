#!/usr/bin/env python3

import cv2
import sys
import os

def detect_faces(image_path, output_path="output.jpg"):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found or cannot be opened.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(output_path, image)

    print(f"Detected {len(faces)} face(s). Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python face_detector.py <image_path> [output_path]")
        sys.exit(1)

    img_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output.jpg"

    detect_faces(img_path, out_path)