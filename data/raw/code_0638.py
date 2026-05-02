"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
import pyttsx3  # Text-to-speech library
import pdfplumber  # PDF parsing library
from PyPDF2 import PdfReader  # PDF reading library
import webbrowser  # Web browser control library
from bs4 import BeautifulSoup  # HTML parsing library
import requests  # HTTP request library
import time  # Time handling library
import os  # Operating system handling library

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define a function to read text from a PDF file
def read_pdf(file_path):
    try:
        # Open the PDF file
        pdf = PdfReader(file_path)
        
        # Extract text from each page
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        
        # Return the extracted text
        return text
    
    except Exception as e:
        print(f"Error reading PDF: {e}")

# Define a function to read text from a document
def read_document(file_path):
    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            # Extract text from each page
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        
        # Return the extracted text
        return text
    
    except Exception as e:
        print(f"Error reading document: {e}")

# Define a function to read text from a web page
def read_webpage(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the text from the HTML content
            text = soup.get_text()
            
            # Return the extracted text
            return text
        
        else:
            print(f"Failed to retrieve webpage: {response.status_code}")
    
    except Exception as e:
        print(f"Error reading webpage: {e}")

# Define a function to read text from a file
def read_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the file content
            text = file.read()
            
            # Return the file content
            return text
    
    except Exception as e:
        print(f"Error reading file: {e}")

# Test the functions
pdf_file_path = 'example.pdf'
document_file_path = 'example.docx'
webpage_url = 'https://www.example.com'
file_path = 'example.txt'

if __name__ == "__main__":
    print("Reading PDF...")
    pdf_text = read_pdf(pdf_file_path)
    engine.say(pdf_text)
    engine.runAndWait()
    
    print("\nReading document...")
    document_text = read_document(document_file_path)
    engine.say(document_text)
    engine.runAndWait()
    
    print("\nReading webpage...")
    webpage_text = read_webpage(webpage_url)
    engine.say(webpage_text)
    engine.runAndWait()
    
    print("\nReading file...")
    file_text = read_file(file_path)
    engine.say(file_text)
    engine.runAndWait()