import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image
import torch.nn as nn

# Define the simplified model class
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

# Instantiate the model
loaded_model = RoadSignCNN(num_classes=4)  # Provide the number of classes

# Load the state dictionary
loaded_model.load_state_dict(torch.load('traffic_model.pth', map_location='cpu'))

loaded_model.eval()

# Define transforms and create the dataset
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Assuming you have a separate 'test_images' folder for testing
test_dataset = datasets.ImageFolder(root='test_images', transform=transform)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

def sign_prediction(input_path):
    image = Image.open(input_path).convert('RGB')
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = loaded_model(image)

    _, predicted_class = torch.max(output, 1)
    predicted_class_label = test_dataset.classes[predicted_class.item()]
    print(f'File: {os.path.basename(input_path)}, Predicted Class: {predicted_class_label}')
    return predicted_class_label


