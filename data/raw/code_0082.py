#!/usr/bin/env python3

import sys
import json
import cv2
import easyocr


def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or invalid path")
    return image


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    return gray


def extract_handwritten_text(image):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image)

    output = []
    for bbox, text, confidence in results:
        output.append({
            "text": text,
            "confidence": float(confidence),
            "bbox": bbox
        })

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python handwriting_ocr.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    image = load_image(image_path)
    processed = preprocess(image)

    results = extract_handwritten_text(processed)

    print(json.dumps({
        "results": results
    }, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()