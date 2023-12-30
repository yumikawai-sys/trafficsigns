import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Define the CNN model
class RoadSignCNN(nn.Module):
    def __init__(self, num_classes):
        super(RoadSignCNN, self).__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Flatten(),
            nn.Linear(64 * 56 * 56, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.layers(x)

# Define transforms and create datasets
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Assuming you have separate folders for each class within the 'training_images' directory
training_dataset = datasets.ImageFolder(root='training_images', transform=transform)

# Use DataLoader for batching
training_loader = DataLoader(training_dataset, batch_size=1, shuffle=False)

# Instantiate the model
model = RoadSignCNN(num_classes=len(training_dataset.classes))

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model on test data (for demonstration purposes)
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for inputs, labels in training_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Save the trained model state dictionary
torch.save(model.state_dict(), 'traffic_model.pth')

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torchvision.transforms.functional import to_tensor

# Define the CNN model
class RoadSignCNN(nn.Module):
    def __init__(self, num_classes):
        super(RoadSignCNN, self).__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Flatten(),
            nn.Linear(64 * 56 * 56, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.layers(x)

# Function to calculate mean and standard deviation of a dataset
def calculate_mean_std(dataset):
    channels_sum, channels_squared_sum, num_batches = 0, 0, 0

    for data in dataset:
        inputs, _ = data
        channels_sum += torch.mean(inputs, dim=[0, 1, 2])
        channels_squared_sum += torch.mean(inputs ** 2, dim=[0, 1, 2])
        num_batches += 1

    mean = channels_sum / num_batches
    std = (channels_squared_sum / num_batches - mean ** 2) ** 0.5

    return mean, std


# Define transforms and create datasets
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Assuming you have separate folders for each class within the 'training_images' directory
training_dataset = datasets.ImageFolder(root='training_images', transform=transform)

# Calculate mean and standard deviation
mean, std = calculate_mean_std(training_dataset)
print("Mean:", mean)
print("Standard Deviation:", std)

# Update the transform for test images with normalization
transform_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=mean, std=std)
])

# Assuming you have a separate 'test_images' folder for testing
test_dataset = datasets.ImageFolder(root='test_images', transform=transform_test)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

# Create the training data loader
training_loader = DataLoader(training_dataset, batch_size=1, shuffle=False)

# Instantiate the model
model = RoadSignCNN(num_classes=len(training_dataset.classes))

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model on test data (for demonstration purposes)
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for inputs, labels in training_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Save the trained model state dictionary
torch.save(model.state_dict(), 'traffic_model.pth')

