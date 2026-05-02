"""
Auto-generated Python code
Scenario : Machine Learning - AI Model Deployment
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision
import torchvision.transforms as transforms
import os
import numpy as np
from PIL import Image

# Set device to GPU if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Define a custom dataset class for image classification
class ImageDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image_path = self.image_paths[index]
        label = self.labels[index]

        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)

        # Convert label to tensor
        label = torch.tensor(label, dtype=torch.long)

        return image, label

# Load dataset and define transforms
transform = transforms.Compose([transforms.Resize((224, 224)),
                                transforms.ToTensor(),
                                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg', ...]
labels = [0, 1, ...]  # corresponding labels for each image

dataset = ImageDataset(image_paths, labels, transform)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define a simple neural network model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, kernel_size=3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=3)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Initialize the model, optimizer and loss function
model = Net()
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
for epoch in range(10):
    for i, (images, labels) in enumerate(data_loader):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Save the model to a file for later use
torch.save(model.state_dict(), 'model.pth')

# Load the saved model and run inference on a new image
def run_inference(image_path):
    try:
        # Load the model from the saved file
        model.load_state_dict(torch.load('model.pth'))
        model.eval()

        # Load the new image
        image = Image.open(image_path)
        image = transform(image)
        image = image.unsqueeze(0).to(device)

        # Run the inference
        output = model(image)
        _, predicted = torch.max(output, 1)

        return predicted.item()
    except Exception as e:
        print(f"Error running inference: {str(e)}")

# Example usage:
new_image_path = 'path/to/new/image.jpg'
predicted_class = run_inference(new_image_path)
print(f"Predicted class: {predicted_class}")