"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_002.txt
Run      : 1
"""

# Import necessary libraries
import torch
from PIL import Image
import os
import pandas as pd

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Function to perform object detection
def detect_objects(image_path):
    try:
        # Open the image
        img = Image.open(image_path)

        # Perform inference
        results = model(img)

        # Print results
        results.print()  # Output class names and confidences

        # Display results
        results.show()

        # Convert results to pandas DataFrame
        df = results.pandas().xyxy[0]

        return df

    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the image path
image_path = 'path/to/your/image.jpg'
result_df = detect_objects(image_path)

# Output detected objects
if result_df is not None:
    print("Detected objects:")
    print(result_df)

    # You can save the detected output if needed
    # results.save(save_dir=os.path.join('output'))
else:
    print("No objects detected or an error occurred.")