import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image

import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from PIL import Image

# Load the trained model for prediction
loaded_model = torch.load('traffic_model.pth', map_location='cpu')  # Add map_location argument if running on CPU
loaded_model.eval()

# Define transforms and create the dataset
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Assuming you have a separate 'test_images' folder for testing
test_dataset = datasets.ImageFolder(root='test_images', transform=transform)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

# Predict using the test dataset
for input_path, label in test_dataset.samples:
    # Open the image and convert it to RGB
    image = Image.open(input_path).convert('RGB')
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = loaded_model(image)

    _, predicted_class = torch.max(output, 1)
    predicted_class_label = test_dataset.classes[predicted_class.item()]
    print(f'File: {os.path.basename(input_path)}, Predicted Class: {predicted_class_label}')