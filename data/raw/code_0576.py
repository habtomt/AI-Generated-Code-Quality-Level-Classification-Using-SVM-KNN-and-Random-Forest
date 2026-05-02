"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_000.txt
Run      : 2
"""

from flask import Flask, request, jsonify
from PIL import Image
import io
import os
import numpy as np

app = Flask(__name__)

# Set up API key for your image handling service (e.g. Google Cloud Vision API)
API_KEY = "YOUR_API_KEY"

def process_image(image_data):
    """
    Process and analyze an image using Pillow library.
    """
    try:
        # Load image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Resize image to 800x600 pixels
        img = img.resize((800, 600))
        
        # Convert image to grayscale
        img = img.convert('L')
        
        # Save image to bytes
        output_bytes = io.BytesIO()
        img.save(output_bytes, 'JPEG')
        
        # Get image metadata
        width, height = img.size
        mode = img.mode
        
        return {
            "width": width,
            "height": height,
            "mode": mode,
            "output_bytes": output_bytes.getvalue()
        }
    
    except Exception as e:
        return {
            "error": str(e)
        }

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    """
    Process and analyze an image upon receipt through an HTTP trigger.
    """
    try:
        # Get image data from request body
        image_data = request.files['image'].read()
        
        # Process and analyze image
        result = process_image(image_data)
        
        # Return result as JSON response
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)