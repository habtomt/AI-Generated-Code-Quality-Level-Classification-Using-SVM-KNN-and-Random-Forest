"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import cv2
import numpy as np
from PIL import Image
import pytesseract
import os

# Load the pre-trained license plate detection model
model_path = "license_plate_detection_model.h5"
model = load_model(model_path)

# Load the license plate recognition model
recognition_model_path = "license_plate_recognition_model.h5"
recognition_model = load_model(recognition_model_path)

# Define a function to detect license plates from images
def detect_license_plate(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to segment out the license plate
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours of the license plate
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate over the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Ignore small contours
        if area < 1000:
            continue
        
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Check if the contour is a license plate
        if h > 50 and w > 100:
            # Crop the license plate from the original image
            license_plate = image[y:y+h, x:x+w]
            
            # Resize the license plate to 224x224
            license_plate = cv2.resize(license_plate, (224, 224))
            
            # Convert the license plate to an array
            license_plate = img_to_array(license_plate)
            
            # Normalize the license plate
            license_plate = license_plate / 255.0
            
            # Make predictions using the license plate detection model
            predictions = model.predict(np.array([license_plate]))
            
            # Check if the license plate is detected
            if np.max(predictions) > 0.5:
                # Get the predicted class
                class_index = np.argmax(predictions)
                
                # Get the class label
                class_label = class_index
                
                # Return the detected license plate
                return class_label
    
    # Return None if no license plate is detected
    return None

# Define a function to recognize license plates from images
def recognize_license_plate(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Detect the license plate
    license_plate = detect_license_plate(image_path)
    
    # If no license plate is detected, return None
    if license_plate is None:
        return None
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to segment out the license plate
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours of the license plate
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate over the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Ignore small contours
        if area < 1000:
            continue
        
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Check if the contour is a license plate
        if h > 50 and w > 100:
            # Crop the license plate from the original image
            license_plate = image[y:y+h, x:x+w]
            
            # Convert the license plate to a PIL image
            license_plate = Image.fromarray(license_plate)
            
            # Apply OCR to the license plate
            text = pytesseract.image_to_string(license_plate)
            
            # Return the recognized license plate
            return text
    
    # Return None if no license plate is recognized
    return None

# Test the functions
image_path = "test_image.jpg"
print("Detected license plate:", detect_license_plate(image_path))
print("Recognized license plate:", recognize_license_plate(image_path))