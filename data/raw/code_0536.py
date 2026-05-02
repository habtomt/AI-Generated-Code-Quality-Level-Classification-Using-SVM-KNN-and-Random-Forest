"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_003.txt
Run      : 2
"""

from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import pyttsx3
import os

# Set up Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up engine for text-to-speech
engine = pyttsx3.init()

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.
    """
    try:
        # Open the image using OpenCV
        image = cv2.imread(image_path)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply binary threshold to segment the text
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Perform OCR on the text
        text = pytesseract.image_to_string(thresh)
        
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def extract_personal_info(text):
    """
    Extracts personal information from the text.
    """
    try:
        # Use regular expressions to extract the information
        name = re.search(r'Name: (.*)', text, re.IGNORECASE)
        birthdate = re.search(r'DOB: (.*)', text, re.IGNORECASE)
        address = re.search(r'Address: (.*)', text, re.IGNORECASE)
        identification_number = re.search(r'ID No: (.*)', text, re.IGNORECASE)
        
        # Return the extracted information as a dictionary
        return {
            'name': name.group(1) if name else None,
            'birthdate': birthdate.group(1) if birthdate else None,
            'address': address.group(1) if address else None,
            'identification_number': identification_number.group(1) if identification_number else None
        }
    except Exception as e:
        print(f"Error extracting personal info: {e}")
        return None

def speak_info(info):
    """
    Speaks the extracted information using text-to-speech.
    """
    try:
        # Speak the information
        engine.say(f"Name: {info['name']}, DOB: {info['birthdate']}, Address: {info['address']}, ID No: {info['identification_number']}")
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking info: {e}")

def main():
    # Specify the path to the image
    image_path = r'C:\path\to\image.jpg'
    
    # Extract text from the image
    text = extract_text_from_image(image_path)
    
    # Extract personal information from the text
    info = extract_personal_info(text)
    
    # Speak the extracted information
    speak_info(info)

if __name__ == "__main__":
    main()