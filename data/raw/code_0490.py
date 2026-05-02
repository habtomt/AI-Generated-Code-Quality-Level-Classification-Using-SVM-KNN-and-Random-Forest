"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_003.txt
Run      : 1
"""

from PIL import Image
import os

def reduce_image_size(input_path, output_path, quality=85):
    """
    Reduces the file size of an image while maintaining its quality.
    - input_path: str, Path to the input image file.
    - output_path: str, Path where the output image will be saved.
    - quality: int, The image quality percentage for output JPEG (1-100).
               Default is 85, which is a good balance between quality and size.
    """
    try:
        # Open an image file
        with Image.open(input_path) as img:
            # Check the image format
            if img.format == 'JPEG' or img.format == 'JPG':
                # For JPEG use lossy compression
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            elif img.format == 'PNG':
                # For PNG use lossless compression
                img.save(output_path, 'PNG', optimize=True)
            else:
                # For other formats save in PNG format to compress
                img.save(output_path, 'PNG', optimize=True)
        print(f"Image successfully compressed and saved at: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
reduce_image_size('path/to/input/image.jpg', 'path/to/output/image.jpg', quality=75)