"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_001.txt
Run      : 1
"""

from PIL import Image, ImageEnhance

def enhance_image(input_image_path, output_image_path, brightness=1.0, contrast=1.0, sharpness=1.0):
    # Open an image file
    try:
        with Image.open(input_image_path) as img:
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)

            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness)

            # Save the modified image
            img.save(output_image_path)
            print(f"Enhanced image saved to {output_image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_image_path = 'input.jpg'
output_image_path = 'output.jpg'

# Set desired enhancement values
brightness_factor = 1.2    # Increase brightness by 20%
contrast_factor = 1.5      # Increase contrast by 50%
sharpness_factor = 2.0     # Double the sharpness

enhance_image(input_image_path, output_image_path, brightness_factor, contrast_factor, sharpness_factor)