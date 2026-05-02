"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import pytesseract
from PIL import Image
import pdf2image
import os
import cv2
import pandas as pd
from datetime import datetime

# Placeholder API key for OCR (can be replaced with actual API key)
# OCR.space API key
ocr_key = "YOUR_OCR_API_KEY"

# Function to extract text from image
def extract_text_from_image(image_path):
    try:
        # Use Tesseract OCR to extract text from image
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_path(pdf_path)
        
        # Extract text from each image
        text = ""
        for image in images:
            text += extract_text_from_image(image.filename)
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")

# Function to extract vendor information
def extract_vendor_info(text):
    try:
        # Use regular expression to find vendor information
        vendor_name = None
        vendor_address = None
        for line in text.splitlines():
            if "Vendor:" in line or "Vendor Name:" in line:
                vendor_name = line.split(":")[1].strip()
            elif "Address:" in line:
                vendor_address = line.split(":")[1].strip()
        
        return vendor_name, vendor_address
    except Exception as e:
        print(f"Error extracting vendor information: {e}")

# Function to extract invoice details
def extract_invoice_details(text):
    try:
        # Use regular expression to find invoice details
        invoice_number = None
        invoice_date = None
        for line in text.splitlines():
            if "Invoice Number:" in line:
                invoice_number = line.split(":")[1].strip()
            elif "Invoice Date:" in line:
                invoice_date = line.split(":")[1].strip()
        
        return invoice_number, invoice_date
    except Exception as e:
        print(f"Error extracting invoice details: {e}")

# Function to extract item descriptions and prices
def extract_item_descriptions_and_prices(text):
    try:
        # Use regular expression to find item descriptions and prices
        items = []
        for line in text.splitlines():
            if "Item" in line or "Description" in line:
                items.append(line.split(":")[1].strip())
        
        return items
    except Exception as e:
        print(f"Error extracting item descriptions and prices: {e}")

# Function to extract data from OCR.space API
def extract_data_from_ocr_space_api(image_path, api_key):
    try:
        # Send image to OCR.space API
        url = f"https://api.ocr.space/parse/image"
        params = {
            "isOverlayRequired": "true",
            "language": "eng",
            "apikey": api_key
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "url": f"https://api.ocr.space/parse/image?isOverlayRequired=true&language=eng&apikey={api_key}&url={image_path}"
        }
        
        # Make API call
        response = requests.post(url, headers=headers, json=data, params=params)
        
        # Parse JSON response
        data = response.json()
        
        # Extract text from response
        text = data["ParsedResults"][0]["ParsedText"]
        
        return text
    except Exception as e:
        print(f"Error extracting data from OCR.space API: {e}")

# Main function
def main():
    # Set image path
    image_path = "invoice.png"
    
    # Extract text from image using OCR.space API
    text = extract_data_from_ocr_space_api(image_path, ocr_key)
    
    # Extract vendor information
    vendor_name, vendor_address = extract_vendor_info(text)
    
    # Extract invoice details
    invoice_number, invoice_date = extract_invoice_details(text)
    
    # Extract item descriptions and prices
    items = extract_item_descriptions_and_prices(text)
    
    # Create DataFrame
    df = pd.DataFrame({
        "Vendor Name": [vendor_name],
        "Vendor Address": [vendor_address],
        "Invoice Number": [invoice_number],
        "Invoice Date": [invoice_date],
        "Item Description": items
    })
    
    # Print DataFrame
    print(df)

# Run main function
if __name__ == "__main__":
    main()