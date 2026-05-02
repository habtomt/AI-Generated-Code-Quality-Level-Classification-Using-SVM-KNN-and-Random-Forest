"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_003.txt
Run      : 1
"""

# Required imports
import cv2
import pytesseract
import numpy as np
import re
from PIL import Image
import imutils

def extract_text_from_id_card(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Optionally, preprocess the image (e.g., convert to gray-scale, adjust contrast)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Reduce noise

    # Use OCR to extract text
    custom_config = r'--oem 3 --psm 6'  # You can change the configuration
    extracted_text = pytesseract.image_to_string(gray, config=custom_config)

    return extracted_text

def extract_fields(extracted_text):
    # Use regular expressions to extract specific fields
    fields = {
        'name': re.search(r'Name: (\w+\s\w+)', extracted_text).group(1),
        'birthdate': re.search(r'DOB: (\d{2}/\d{2}/\d{4})', extracted_text).group(1),
        'address': re.search(r'Address: (\w+\s\w+\s\d+\s\w+)', extracted_text).group(1),
        'identification_number': re.search(r'ID Number: (\d+)', extracted_text).group(1)
    }

    return fields

def preprocess_image(image_path):
    # Optional: Resize the image to a fixed size for better OCR results
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=800)

    return image

def main():
    try:
        # Specify the path to the ID card image
        image_path = 'path_to_your_id_card_image.jpg'
        
        # Adjust path if necessary for Tesseract
        # pytesseract.pytesseract.tesseract_cmd = r'path_to_your_tesseract_executable'

        # Preprocess the image
        image = preprocess_image(image_path)

        # Extract text from the ID card
        extracted_text = extract_text_from_id_card(image_path)

        # Extract specific fields from the extracted text
        fields = extract_fields(extracted_text)

        # Print the extracted fields
        print("Extracted Information:")
        print(f"Name: {fields['name']}")
        print(f"Birthdate: {fields['birthdate']}")
        print(f"Address: {fields['address']}")
        print(f"Identification Number: {fields['identification_number']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()