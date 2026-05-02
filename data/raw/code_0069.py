#!/usr/bin/env python3

import sys
from PIL import Image

def compress_image(image_path, output_path="compressed.jpg", quality=85, optimize=True):
    img = Image.open(image_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img.save(output_path, "JPEG", quality=quality, optimize=optimize)
    print(f"Compressed image saved to {output_path}")

def compress_lossless(image_path, output_path="compressed.png"):
    img = Image.open(image_path)
    img.save(output_path, "PNG", optimize=True)
    print(f"Lossless compressed image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python img_compress.py lossy <input> <output> [quality]")
        print("  python img_compress.py lossless <input> <output>")
        sys.exit(1)

    mode = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output.jpg"

    if mode == "lossy":
        q = int(sys.argv[4]) if len(sys.argv) > 4 else 85
        compress_image(input_path, output_path, quality=q)
    elif mode == "lossless":
        compress_lossless(input_path, output_path)
    else:
        print("Invalid mode. Use 'lossy' or 'lossless'.")