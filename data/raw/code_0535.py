"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries for image processing and OCR
import cv2
import pytesseract
from PIL import Image
import numpy as np

# Set path to Tesseract OCR engine executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from an image
def extract_text_from_image(image_path):
    try:
        # Open image using OpenCV
        image = cv2.imread(image_path)
        
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Perform OCR on the image
        text = pytesseract.image_to_string(gray_image)
        
        return text
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to extract text from a screenshot
def extract_text_from_screenshot():
    try:
        # Get a screenshot of the active window
        img = pyautogui.screenshot()
        
        # Convert the screenshot to a numpy array
        frame = np.array(img)
        
        # Extract text from the screenshot
        text = pytesseract.image_to_string(frame)
        
        return text
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to extract text from a digital input (e.g. a file)
def extract_text_from_file(file_path):
    try:
        # Open the file using Pillow
        image = Image.open(file_path)
        
        # Extract text from the file
        text = pytesseract.image_to_string(image)
        
        return text
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Extract text from an image
    image_path = 'path_to_your_image.jpg'
    text = extract_text_from_image(image_path)
    if text:
        print("Text extracted from image:")
        print(text)

    # Extract text from a screenshot
    text = extract_text_from_screenshot()
    if text:
        print("\nText extracted from screenshot:")
        print(text)

    # Extract text from a digital input (e.g. a file)
    file_path = 'path_to_your_file.pdf'
    text = extract_text_from_file(file_path)
    if text:
        print("\nText extracted from file:")
        print(text)