"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_003.txt
Run      : 3
"""

from PIL import Image
import os

def compress_image(image_path, output_path, quality=80):
    """
    Compress an image while maintaining its quality.

    Args:
        image_path (str): Path to the image file.
        output_path (str): Path where the compressed image will be saved.
        quality (int, optional): Quality of the compressed image. Defaults to 80.
    """
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found")

    try:
        # Open the image using PIL
        with Image.open(image_path) as img:
            # Get the format of the image
            format = img.format

            # Save the image with the specified quality
            img.save(output_path, format, quality=quality)

            # Print a success message
            print(f"Image compressed and saved to {output_path}")
    except Exception as e:
        # Handle any exceptions that occur during compression
        print(f"Error compressing image: {e}")


# Example usage
if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"
    output_path = "compressed_image.jpg"
    compress_image(image_path, output_path)