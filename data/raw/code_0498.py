"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
from PIL import Image, ImageEnhance
import os

# Define a function to adjust image quality
def adjust_image_quality(image_path, output_path):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Adjust brightness
        enhancer = ImageEnhance.Brightness(image)
        image_brightness = enhancer.enhance(1.2)  # Increase brightness by 20%

        # Adjust contrast
        enhancer = ImageEnhance.Contrast(image_brightness)
        image_contrast = enhancer.enhance(1.2)  # Increase contrast by 20%

        # Adjust sharpness
        enhancer = ImageEnhance.Sharpness(image_contrast)
        image_sharpness = enhancer.enhance(1.2)  # Increase sharpness by 20%

        # Save the adjusted image
        image_sharpness.save(output_path)

        print(f"Image quality adjusted and saved to {output_path}")

    except Exception as e:
        print(f"Error adjusting image quality: {e}")

# Example usage
image_path = "input.jpg"  # Replace with your input image path
output_path = "output.jpg"  # Replace with your desired output image path
adjust_image_quality(image_path, output_path)