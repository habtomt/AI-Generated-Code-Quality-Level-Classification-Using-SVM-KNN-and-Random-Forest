#!/usr/bin/env python3

import sys
from PIL import Image, ImageEnhance

def enhance_image(image_path, output_path="enhanced.jpg",
                  brightness=1.0, contrast=1.0, sharpness=1.0):

    image = Image.open(image_path)

    image = ImageEnhance.Brightness(image).enhance(brightness)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = ImageEnhance.Sharpness(image).enhance(sharpness)

    image.save(output_path)
    print(f"Saved enhanced image to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_enhance.py <image_path> [output_path] [brightness] [contrast] [sharpness]")
        sys.exit(1)

    img_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "enhanced.jpg"

    brightness = float(sys.argv[3]) if len(sys.argv) > 3 else 1.2
    contrast = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
    sharpness = float(sys.argv[5]) if len(sys.argv) > 5 else 1.2

    enhance_image(img_path, out_path, brightness, contrast, sharpness)