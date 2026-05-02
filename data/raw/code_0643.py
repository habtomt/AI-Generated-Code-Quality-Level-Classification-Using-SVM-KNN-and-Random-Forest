"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import pyttsx3  # Text-to-speech library
import PyPDF2  # Library to read PDF files
from PIL import Image  # Library to read images
import pytesseract  # Optical Character Recognition (OCR) library
from bs4 import BeautifulSoup  # Library to parse HTML documents
import requests  # Library to send HTTP requests

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to read text from a URL
def read_from_url(url):
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from the HTML content
        text = soup.get_text()
        
        # Speak the extracted text
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to read text from a PDF file
def read_from_pdf(file_path):
    try:
        # Open the PDF file
        pdf_file = open(file_path, 'rb')
        
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from the PDF file
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Speak the extracted text
        engine.say(text)
        engine.runAndWait()
        
        # Close the PDF file
        pdf_file.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to read text from an image file
def read_from_image(file_path):
    try:
        # Read the image file using Pillow
        image = Image.open(file_path)
        
        # Convert the image to text using OCR
        text = pytesseract.image_to_string(image)
        
        # Speak the extracted text
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Read text from a URL
read_from_url('https://www.example.com')

# Read text from a PDF file
read_from_pdf('path/to/example.pdf')

# Read text from an image file
read_from_image('path/to/example.png')