"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_000.txt
Run      : 3
"""

# Import required libraries
import PyPDF2
import re
import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
from tkinter import tk
from tkinter import filedialog

# Set up Pytesseract for OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from scanned or photographed invoices
def extract_invoice_details(image_path):
    try:
        # Open the image using OpenCV
        image = cv2.imread(image_path)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to enhance the image quality
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Save the processed image
        cv2.imwrite('processed_image.png', thresh)
        
        # Use Tesseract OCR to extract text from the image
        text = pytesseract.image_to_string(Image.open('processed_image.png'), lang='eng')
        
        # Extract relevant details from the text
        invoice_number = re.search(r'Invoice No.: (\d+)', text).group(1)
        date = re.search(r'Date: (\d{1,2}/\d{1,2}/\d{2,4})', text).group(1)
        vendor_name = re.search(r'Bill To: (.*)', text).group(1)
        items = re.findall(r'\d+\.\d+ \- (.*)\n', text)
        prices = re.findall(r'\d+\.\d+ \- (.*)', text)
        
        # Print the extracted details
        print(f'Invoice Number: {invoice_number}')
        print(f'Date: {date}')
        print(f'Vendor Name: {vendor_name}')
        for item, price in zip(items, prices):
            print(f'Item: {item}, Price: {price}')
        
    except Exception as e:
        print(f'Error: {e}')

# Function to open file dialog to select image file
def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    return file_path

# Main function
def main():
    # Open file dialog to select image file
    image_path = open_file_dialog()
    
    # Extract invoice details from the selected image
    extract_invoice_details(image_path)

if __name__ == "__main__":
    main()