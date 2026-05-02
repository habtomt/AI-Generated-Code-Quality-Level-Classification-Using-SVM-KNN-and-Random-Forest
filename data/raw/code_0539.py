"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import cv2
import pytesseract
from PIL import Image
import numpy as np

# Placeholder API key for Google Cloud Vision API
VISION_API_KEY = "YOUR_GOOGLE_CLOUD_VISION_API_KEY"

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Google Cloud Vision API
    """
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to the grayscale image to segment text
        _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # Save the thresholded image
        cv2.imwrite("thresholded_image.png", thresh_image)
        
        # Use Tesseract-OCR to extract text from the image
        text = pytesseract.image_to_string(Image.open("thresholded_image.png"))
        
        return text
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_text_from_input():
    """
    Extracts text from digital input (e.g., keyboard)
    """
    try:
        # Get user input
        text = input("Enter text: ")
        
        return text
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    # Choose the input method
    input_method = input("Do you want to (1) take a photo or (2) enter text manually? ")
    
    if input_method == "1":
        # Get the image path
        image_path = input("Enter the path to the image: ")
        
        # Extract text from the image
        text = extract_text_from_image(image_path)
        
    elif input_method == "2":
        # Extract text from digital input
        text = extract_text_from_input()
    
    else:
        print("Invalid input method")
        return
    
    # Print the extracted text
    if text:
        print("Extracted text:")
        print(text)

if __name__ == "__main__":
    main()