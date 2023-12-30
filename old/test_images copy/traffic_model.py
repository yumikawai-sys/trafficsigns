import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image


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

# Assuming you have separate folders for each class within the 'training_images' and 'test_images' directories
training_dataset = datasets.ImageFolder(root='training_images', transform=transform)
test_dataset = datasets.ImageFolder(root='test_images', transform=transform)

# Use DataLoader for batching
training_loader = DataLoader(training_dataset, batch_size=1, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

# Instantiate the model
model = RoadSignCNN(num_classes=len(training_dataset.classes))

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model on the training data
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for inputs, labels in training_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Save the entire model
torch.save(model, 'traffic_model.pth')

# Load the trained model for prediction
loaded_model = RoadSignCNN(num_classes=len(training_dataset.classes))
loaded_model = torch.load('traffic_model.pth')
loaded_model.eval()

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
