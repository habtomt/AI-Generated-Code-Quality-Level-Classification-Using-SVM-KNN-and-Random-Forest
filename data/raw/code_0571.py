"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_000.txt
Run      : 1
"""

# Import necessary libraries
import base64
from io import BytesIO
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Define a function to process and analyze images
def process_image(image_data):
    try:
        # Decode the base64 image
        image_buffer = BytesIO(base64.b64decode(image_data))

        # Open the image using PIL
        image = Image.open(image_buffer)

        # Resize the image
        image = image.resize((200, 200))  # Resize to 200x200 for example

        # Apply a grayscale filter
        image = image.convert('L')

        # Enhance the contrast of the image
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # Enhance the contrast by 50%

        # Apply a blur filter
        image = image.filter(ImageFilter.GaussianBlur(radius=2))

        # Convert the image back to a base64 string
        image_buffer = BytesIO()
        image.save(image_buffer, format='PNG')
        image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')

        # Return the processed image as a base64 string
        return {
            'image': image_data
        }
    except Exception as e:
        return {
            'error': 'Image processing failed',
            'details': str(e)
        }

# Define a route to handle HTTP requests
@app.route('/process_image', methods=['POST'])
def handle_request():
    try:
        # Get the image data from the request
        image_data = request.get_json()['image']

        # Process and analyze the image
        result = process_image(image_data)

        # Return the result as a JSON response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'error': 'Invalid request',
            'details': str(e)
        }), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)