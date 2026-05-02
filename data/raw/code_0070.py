#!/usr/bin/env python3

import sys
import cv2
import numpy as np

def segment_image_kmeans(image_path, k=4, output_path="segmented.jpg"):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not load image.")
        return

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixel_values = img.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    _, labels, centers = cv2.kmeans(
        pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img.shape)

    result = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, result)

    print(f"Segmented image saved to {output_path}")

def split_image_grid(image_path, rows=2, cols=2, output_prefix="part"):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not load image.")
        return

    h, w = image.shape[:2]
    dh, dw = h // rows, w // cols

    count = 0
    for i in range(rows):
        for j in range(cols):
            part = image[i*dh:(i+1)*dh, j*dw:(j+1)*dw]
            out_path = f"{output_prefix}_{count}.jpg"
            cv2.imwrite(out_path, part)
            count += 1

    print(f"Image split into {count} parts.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python img_segment.py kmeans <image> <k> <output>")
        print("  python img_segment.py grid <image> <rows> <cols> <prefix>")
        sys.exit(1)

    mode = sys.argv[1]
    image_path = sys.argv[2]

    if mode == "kmeans":
        k = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        out = sys.argv[4] if len(sys.argv) > 4 else "segmented.jpg"
        segment_image_kmeans(image_path, k, out)

    elif mode == "grid":
        rows = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        cols = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        prefix = sys.argv[5] if len(sys.argv) > 5 else "part"
        split_image_grid(image_path, rows, cols, prefix)

    else:
        print("Invalid mode. Use 'kmeans' or 'grid'.")