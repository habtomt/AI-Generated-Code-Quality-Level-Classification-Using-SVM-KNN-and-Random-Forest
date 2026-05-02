#!/usr/bin/env python3

import cv2
import sys
import numpy as np

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

def detect_objects(image_path, prototxt, model, output_path="output.jpg", confidence_threshold=0.5):
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confidence_threshold:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            color = COLORS[idx]
            cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)

            text = f"{label}: {confidence:.2f}"
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(image, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imwrite(output_path, image)
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python object_detect.py <image> <prototxt> <model> [output]")
        sys.exit(1)

    image_path = sys.argv[1]
    prototxt_path = sys.argv[2]
    model_path = sys.argv[3]
    output_path = sys.argv[4] if len(sys.argv) > 4 else "output.jpg"

    detect_objects(image_path, prototxt_path, model_path, output_path)