"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
from PIL import Image
import cv2
import numpy as np

def adjust_image(image_path, output_path):
    # Open the image using Pillow library
    img = Image.open(image_path)

    # Convert the image to numpy array for OpenCV operations
    img_array = np.array(img)

    # Convert the image to HSV color space
    hsv_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV)

    # Adjust brightness
    # Increase brightness by 50%
    # Note: Brightness adjustment is done in HSV color space
    hsv_img[..., 2] = np.clip(hsv_img[..., 2] * 1.5, 0, 255)  # Increase brightness

    # Adjust contrast
    # Increase contrast by 50%
    contrast_factor = 1.5
    adjusted_img = cv2.convertScaleAbs(hsv_img, alpha=contrast_factor, beta=0)

    # Adjust sharpness
    # Apply unsharp masking
    blurred_img = cv2.GaussianBlur(adjusted_img, (5, 5), 0)
    sharpness_adjusted_img = cv2.addWeighted(adjusted_img, 1.5, blurred_img, -0.5, 0)

    # Convert back to BGR color space and save the image
    output_img = cv2.cvtColor(sharpness_adjusted_img, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path, output_img)

def main():
    try:
        image_path = "input.jpg"  # Replace with your image path
        output_path = "output.jpg"  # Replace with your desired output path
        adjust_image(image_path, output_path)
        print(f"Image adjusted and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()