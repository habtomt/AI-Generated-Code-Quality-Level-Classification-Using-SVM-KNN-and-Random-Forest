"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_000.txt
Run      : 3
"""

from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import VGG16, ResNet50
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

# Model definitions
vgg16_model = VGG16(weights='imagenet', include_top=True)
resnet50_model = ResNet50(weights='imagenet', include_top=True)

def process_image(image_data):
    # Load image from base64 encoded string
    img_bytes = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(img_bytes))

    # Resize the image to 224x224 pixels (compatible with VGG16 and ResNet50)
    img = img.resize((224, 224))

    # Convert image to numpy array
    img_array = np.array(img)

    # Apply a simple filter to the image (e.g. blur)
    img_array = cv2.GaussianBlur(img_array, (5, 5), 0)

    # Preprocess the image for classification
    img_array = image.img_to_array(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Classify the image using VGG16 and ResNet50
    vgg16_preds = decode_predictions(vgg16_model.predict(img_array), top=3)[0]
    resnet50_preds = decode_predictions(resnet50_model.predict(img_array), top=3)[0]

    return vgg16_preds, resnet50_preds

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        # Get the image data from the request body
        image_data = request.json['image']

        # Process the image
        vgg16_preds, resnet50_preds = process_image(image_data)

        # Return the classification results
        return jsonify({
            'VGG16': [
                {'class_name': pred[1], 'probability': pred[2], 'class_id': pred[3]}
                for pred in vgg16_preds
            ],
            'ResNet50': [
                {'class_name': pred[1], 'probability': pred[2], 'class_id': pred[3]}
                for pred in resnet50_preds
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)