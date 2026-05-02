"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_004.txt
Run      : 2
"""

import numpy as np
from PIL import Image
import cv2

# Define the function to divide an image into regions
def divide_image_into_regions(image_path, num_regions, region_size):
    """
    Divide an image into multiple regions of equal size.

    Args:
    - image_path (str): Path to the image file
    - num_regions (int): Number of regions to divide the image into
    - region_size (int): Size of each region

    Returns:
    - A list of NumPy arrays representing the divided regions
    """

    # Load the image
    image = cv2.imread(image_path)

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Calculate the size of each region
    region_width = width // num_regions
    region_height = height // num_regions

    # Initialize an empty list to store the regions
    regions = []

    # Iterate over each region
    for i in range(num_regions):
        for j in range(num_regions):
            # Calculate the top-left and bottom-right coordinates of the region
            x1, y1 = j * region_width, i * region_height
            x2, y2 = (j + 1) * region_width, (i + 1) * region_height

            # Clip the coordinates to ensure they don't exceed the image bounds
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width, x2)
            y2 = min(height, y2)

            # Extract the region from the image
            region = image[y1:y2, x1:x2]

            # Append the region to the list
            regions.append(region)

    return regions

# Usage example
image_path = 'path_to_your_image.jpg'
num_regions = 4
region_size = 256

try:
    regions = divide_image_into_regions(image_path, num_regions, region_size)
    for i, region in enumerate(regions):
        print(f'Region {i+1}:')
        # Display the region using OpenCV
        cv2.imshow('Region', region)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
except Exception as e:
    print(f'Error: {str(e)}')