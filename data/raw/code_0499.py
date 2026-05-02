"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
from PIL import Image

# Load OpenCV and set the directory path for model and image files
cv2_dir = cv2.__path__[0]

# Specify the directory path for the model
model_path = cv2_dir + '/object_detection/ssd_mobilenet_v2_coco_2018_03_29/model.pb'

# Load the pre-trained object detection model
net = cv2.dnn.readNetFromTensorflow(model_path, cv2_dir + '/object_detection/ssd_mobilenet_v2_coco_2018_03_29/pb.txt')

# Load the image
img = cv2.imread('image.jpg')

# Get image dimensions
(h, w) = img.shape[:2]

# Define the minimum probability to filter weak detections
min_confidence = 0.5

# Define the threshold for non-maxima suppression
threshold = 0.3

# Load the pre-trained model
model = load_model('cnn_model.h5')

# Define the classes and their corresponding labels
classes = ['airplane', 'bird', 'car', 'cat', 'dog']

# Detect objects within the image using the pre-trained model
blob = cv2.dnn.blobFromImage(img, 1/127.5, (300, 300), [127.5, 127.5, 127.5], True, False)
net.setInput(blob)
layer_names = net.getLayerNames()
output_layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
outputs = net.forward(output_layer_names)

# Loop through the detections
for output in outputs:
    for detection in output:
        # Extract the scores, class_id, and confidence
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        # Filter out weak detections
        if confidence > min_confidence:
            # Calculate the bounding box coordinates
            box = detection[0:4] * np.array([w, h, w, h])
            (centerX, centerY, width, height) = box.astype('int')
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            # Draw a bounding box around the detected object
            cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(img, classes[class_id], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Preprocess the image for object classification
            img_small = cv2.resize(img[y:y+height, x:x+width], (224, 224))
            img_small = img_small / 255.0

            # Add a batch dimension to the image
            img_small = np.expand_dims(img_small, axis=0)

            # Make predictions using the pre-trained model
            predictions = model.predict(img_small)

            # Display the predicted class
            print(f"Predicted class: {np.argmax(predictions)}")

# Display the image with the detected objects
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()