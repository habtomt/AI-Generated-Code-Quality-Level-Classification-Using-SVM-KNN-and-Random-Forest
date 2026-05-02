#!/usr/bin/env python3

import re
import sys
import json
from PIL import Image
import pytesseract


def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def parse_invoice(text):
    data = {
        "invoice_number": None,
        "date": None,
        "vendor": None,
        "items": [],
        "total": None
    }

    invoice_no = re.search(r"(Invoice\s*(No|Number)?[:\s]*)([A-Z0-9\-]+)", text, re.IGNORECASE)
    if invoice_no:
        data["invoice_number"] = invoice_no.group(3)

    date = re.search(r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text)
    if date:
        data["date"] = date.group(1)

    vendor = re.search(r"(Vendor[:\s]*)(.+)", text, re.IGNORECASE)
    if vendor:
        data["vendor"] = vendor.group(2).strip().split("\n")[0]

    items = re.findall(r"([A-Za-z\s]+)\s+(\d+)\s+([\d\.]+)", text)
    for item in items:
        data["items"].append({
            "description": item[0].strip(),
            "quantity": item[1],
            "price": item[2]
        })

    total = re.search(r"(Total[:\s]*)([\d\.]+)", text, re.IGNORECASE)
    if total:
        data["total"] = total.group(2)

    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python invoice_ocr.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    text = extract_text(image_path)
    parsed_data = parse_invoice(text)

    print(json.dumps({
        "raw_text": text,
        "parsed_data": parsed_data
    }, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()