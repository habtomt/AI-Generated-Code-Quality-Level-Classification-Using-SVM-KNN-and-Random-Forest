"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_002.txt
Run      : 1
"""

# Import required libraries
import cv2
from PIL import Image
import pytesseract
import os

# Set the location of the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

def preprocess_image(image_path):
    """ Preprocess the image for better OCR accuracy. """
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        
        # Check if the image is loaded correctly
        if image is None:
            print(f"Error: Unable to load image {image_path}")
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply a thresholding method to get a binary image
        _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        return binary_image
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def recognize_text(image_path):
    """ Recognize the text from the image. """
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)
        
        if processed_image is None:
            return None
        
        # Convert the processed image to a PIL image
        pil_image = Image.fromarray(processed_image)
        
        # Use Tesseract OCR to recognize the text
        text = pytesseract.image_to_string(pil_image)
        
        return text
    
    except Exception as e:
        print(f"Error recognizing text: {e}")
        return None

# Example usage
image_path = 'handwritten_sample.png'
recognized_text = recognize_text(image_path)

if recognized_text is not None:
    print("Recognized Text:")
    print(recognized_text)