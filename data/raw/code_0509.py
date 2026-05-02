"""
Auto-generated Python code
Scenario : Machine Learning - AI Model Deployment
Prompt   : response_003.txt
Run      : 2
"""

# Import necessary libraries
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import pickle
import mobilenetv2
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load the pre-trained model and its weights
model = mobilenetv2.MobileNetV2()
model.load_state_dict(torch.load('model_weights.pth', map_location=torch.device('cpu')))

# Convert the model to a TensorFlow Lite model
import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model to a file
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

# Import the TensorFlow Lite runtime for Python
import tflite_runtime.interpreter as tflite

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define a function to make predictions
def make_prediction(image_path):
    # Load the image
    image = load_img(image_path, target_size=(224, 224))
    
    # Preprocess the image
    image = img_to_array(image)
    image = preprocess_input(image)
    
    # Convert the image to a TensorFlow Lite-compatible format
    image = np.expand_dims(image, axis=0)
    
    # Set the input tensor value
    interpreter.set_tensor(input_details[0]['index'], image)
    
    # Run the inference
    interpreter.invoke()
    
    # Get the output tensor value
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Return the prediction
    return output_data

# Test the function
image_path = 'test_image.jpg'
prediction = make_prediction(image_path)

# Print the prediction
print(prediction)