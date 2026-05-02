"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_003.txt
Run      : 2
"""

from PIL import Image
import os

def compress_image(image_path, output_path, quality=90):
    """
    Reduce the file size of an image while maintaining its quality.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to the output image file.
        quality (int, optional): Compression quality (1-100). Defaults to 90.

    Raises:
        FileNotFoundError: If the input image file does not exist.
        ValueError: If the output path already exists.
    """

    # Check if the input image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError("Input image file not found.")

    # Check if the output path already exists
    if os.path.exists(output_path):
        raise ValueError("Output path already exists.")

    try:
        # Open the input image file using Pillow
        with Image.open(image_path) as img:
            # Compress the image using lossy compression (JPEG)
            img.save(output_path, 'JPEG', quality=quality)
            print(f"Compressed image saved to {output_path}")
    except Exception as e:
        print(f"Error compressing image: {e}")

# Example usage
input_image = 'path/to/input/image.jpg'
output_image = 'path/to/output/image_compressed.jpg'

compress_image(input_image, output_image)