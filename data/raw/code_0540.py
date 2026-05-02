"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

# Placeholder credentials (replace with your own)
API_KEY = "YOUR_API_KEY"
CUSTOM_OCR_ENGINE = "YOUR_CUSTOM_OCR_ENGINE"

def extract_text_from_image(image_path):
    """
    Extract text from an image using OpenCV and Tesseract OCR.
    """
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to segment the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Save the thresholded image
    cv2.imwrite("thresh.png", thresh)
    
    # Use Tesseract OCR to extract text from the image
    try:
        text = pytesseract.image_to_string(Image.open("thresh.png"), 
                                            lang='eng', 
                                            config=f'--oem {CUSTOM_OCR_ENGINE} --psm 11')
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
    
    return text

def extract_info(text):
    """
    Extract personal information from the extracted text.
    """
    # Use regular expressions to extract relevant information
    pattern = r"(?:Name: )([A-Za-z\s]+)|(?:Birthdate: )([0-9]{2}[/-][0-9]{2}[/-][0-9]{2,4})|(?:Address: )([A-Za-z\s0-9.,]+)|(?:Identification Number: )([0-9]+)"
    matches = re.findall(pattern, text)
    
    # Extract and format the information
    info = {}
    for match in matches:
        if match[0]:
            info["Name"] = match[0].strip()
        if match[1]:
            info["Birthdate"] = match[1].strip()
        if match[2]:
            info["Address"] = match[2].strip()
        if match[3]:
            info["Identification Number"] = match[3].strip()
    
    return info

def main():
    # Specify the path to the identity card image
    image_path = "identity_card.png"
    
    # Extract text from the image
    text = extract_text_from_image(image_path)
    
    # Extract personal information from the text
    info = extract_info(text)
    
    # Print the extracted information
    print(info)

if __name__ == "__main__":
    main()