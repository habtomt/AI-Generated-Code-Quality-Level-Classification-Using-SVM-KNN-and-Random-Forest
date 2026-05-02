"""
Auto-generated Python code
Scenario : Machine Learning - AI Model Deployment
Prompt   : response_002.txt
Run      : 2
"""

# Required imports
import torch
from torch import nn
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
import cv2
import time
from PIL import Image

# Set device to GPU if available, otherwise use CPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Define a lightweight convolutional neural network (CNN) model
class LightweightCNN(nn.Module):
    def __init__(self):
        super(LightweightCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, kernel_size=3)
        self.conv2 = nn.Conv2d(6, 12, kernel_size=3)
        self.fc1 = nn.Linear(12 * 3 * 3, 10)

    def forward(self, x):
        # Apply convolutional layer
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        # Apply another convolutional layer
        x = F.relu(F.max_pool2d(self.conv2(x), 2))
        # Flatten the output
        x = x.view(-1, 12 * 3 * 3)
        # Apply fully connected layer
        x = self.fc1(x)
        return x

# Load the model and move it to the device (GPU or CPU)
model = LightweightCNN()
model.to(device)

# Load the dataset and apply transformations (resize, normalize)
transform = transforms.Compose([transforms.Resize(224),
                                transforms.ToTensor(),
                                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

# Load an example image
img_path = 'your_image.jpg'
img = Image.open(img_path)
img_tensor = transform(img)

# Move the input image to the device (GPU or CPU)
img_tensor = img_tensor.to(device)

# Measure the inference time
start_time = time.time()
# Run the model inference
output = model(img_tensor)
end_time = time.time()

# Calculate the latency
latency = end_time - start_time

# Print the latency
print(f'Latency: {latency} seconds')

# Save the model to a file for future use
torch.save(model.state_dict(), 'lightweight_cnn.pth')

# Load the saved model and run inference again
loaded_model = LightweightCNN()
loaded_model.load_state_dict(torch.load('lightweight_cnn.pth'))
loaded_model.to(device)

# Measure the inference time again
start_time = time.time()
# Run the model inference again
output = loaded_model(img_tensor)
end_time = time.time()

# Calculate the latency
latency = end_time - start_time

# Print the latency
print(f'Latency: {latency} seconds')

# Test the model on a video feed from a camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to a tensor
    frame_tensor = transform(frame)
    frame_tensor = frame_tensor.to(device)

    # Run the model inference
    output = model(frame_tensor)

    # Display the output
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()