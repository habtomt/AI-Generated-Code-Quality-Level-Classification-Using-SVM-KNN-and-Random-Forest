"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_000.txt
Run      : 1
"""

import cv2
import pytesseract
from PIL import Image
import re
import os

# Set the path to the Tesseract OCR executable if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply some preprocessing: thresholding or blurring can help
    processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    return processed_img

def extract_text_from_image(image_path):
    # Preprocess the image to improve OCR accuracy
    processed_img = preprocess_image(image_path)
    
    # Use pytesseract to do OCR on the processed image
    text = pytesseract.image_to_string(processed_img)
    
    return text

def parse_invoice_details(text):
    # This function should implement the logic to parse text and extract invoice details
    invoice_info = {}
    
    # Extract an example: invoice number (assuming a pattern "Invoice No: X" exists in the text)
    invoice_number_match = re.search(r'Invoice\s+No:\s*(\S+)', text, re.IGNORECASE)
    if invoice_number_match:
        invoice_info['invoice_number'] = invoice_number_match.group(1)
    
    # Extract date (assuming a pattern of MM/DD/YYYY or similar exists)
    date_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
    if date_match:
        invoice_info['date'] = date_match.group(1)

    # Add more regular expressions for prices, vendor, and item descriptions as needed
    # For example, to extract prices, you might look for patterns like "$X.XX" or "X.XX"
    price_match = re.findall(r'\$\s*(\d+\.\d+)', text)
    if price_match:
        invoice_info['prices'] = price_match
    
    # To extract vendor information, you might look for patterns like "Vendor: X"
    vendor_match = re.search(r'Vendor:\s*(\S+)', text, re.IGNORECASE)
    if vendor_match:
        invoice_info['vendor'] = vendor_match.group(1)
    
    # To extract item descriptions, you might look for patterns like "Item X: Y"
    item_description_match = re.search(r'Item\s+(\S+):\s*(\S+)', text)
    if item_description_match:
        invoice_info['item_description'] = item_description_match.group(2)
    
    return invoice_info

def main():
    # Check if the image file exists
    image_path = 'path_to_your_invoice_image.jpg'  # Replace with your image path
    if not os.path.isfile(image_path):
        print("Error: Image file not found.")
        return
    
    text = extract_text_from_image(image_path)
    print("Extracted Text:")
    print(text)
    
    invoice_details = parse_invoice_details(text)
    print("Parsed Invoice Details:")
    print(invoice_details)

if __name__ == '__main__':
    main()