#!/usr/bin/env python3

import sys
import json
import re
import cv2
import pytesseract


def load_image(path):
    image = cv2.imread(path)
    if image is None:
        raise ValueError("Image not found")
    return image


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh


def extract_text(image):
    config = "--psm 6"
    text = pytesseract.image_to_string(image, config=config)
    return text


def parse_id_card(text):
    data = {
        "name": None,
        "birthdate": None,
        "id_number": None,
        "address": None,
        "raw_text": text
    }

    name = re.search(r"(Name[:\s]+)([A-Z a-z]+)", text)
    if name:
        data["name"] = name.group(2).strip()

    dob = re.search(r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text)
    if dob:
        data["birthdate"] = dob.group(1)

    id_no = re.search(r"(ID\s*(No|Number)?[:\s]*)([A-Z0-9]+)", text, re.IGNORECASE)
    if id_no:
        data["id_number"] = id_no.group(3)

    address = re.search(r"(Address[:\s]+)(.+)", text)
    if address:
        data["address"] = address.group(2).split("\n")[0].strip()

    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python id_card_ocr.py <image_path>")
        sys.exit(1)

    path = sys.argv[1]

    image = load_image(path)
    processed = preprocess(image)
    text = extract_text(processed)

    result = parse_id_card(text)

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()