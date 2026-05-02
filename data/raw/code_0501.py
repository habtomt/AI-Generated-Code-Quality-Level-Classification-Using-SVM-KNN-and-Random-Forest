"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_004.txt
Run      : 3
"""

# Import necessary libraries
from PIL import Image
import numpy as np

# Define a function to divide an image into multiple parts
def divide_image(image_path, num_rows, num_cols):
    """
    Divide an image into multiple parts or regions.

    Args:
        image_path (str): Path to the input image.
        num_rows (int): Number of rows to divide the image into.
        num_cols (int): Number of columns to divide the image into.

    Returns:
        A 2D list of image segments.
    """

    try:
        # Open the image using Pillow library
        img = Image.open(image_path)

        # Convert the image to a numpy array for easier manipulation
        img_array = np.array(img)

        # Calculate the width and height of each segment
        row_size = img_array.shape[0] // num_rows
        col_size = img_array.shape[1] // num_cols

        # Initialize a 2D list to store the image segments
        image_segments = []

        # Iterate over the number of rows
        for i in range(num_rows):
            # Initialize a list to store the segments in the current row
            row_segments = []

            # Iterate over the number of columns
            for j in range(num_cols):
                # Calculate the start and end indices for the current segment
                start_row = i * row_size
                end_row = (i + 1) * row_size
                start_col = j * col_size
                end_col = (j + 1) * col_size

                # Extract the current segment from the numpy array
                segment = img_array[start_row:end_row, start_col:end_col]

                # Append the segment to the list of row segments
                row_segments.append(segment)

            # Append the list of row segments to the 2D list of image segments
            image_segments.append(row_segments)

        # Return the 2D list of image segments
        return image_segments

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
image_path = "path_to_your_image.jpg"
num_rows = 2
num_cols = 2

image_segments = divide_image(image_path, num_rows, num_cols)

# Print the image segments
for i, row_segments in enumerate(image_segments):
    print(f"Row {i+1}:")
    for j, segment in enumerate(row_segments):
        print(f"  Column {j+1}: Shape = {segment.shape}")