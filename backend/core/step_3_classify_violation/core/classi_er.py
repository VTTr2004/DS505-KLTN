import torch
import torch.nn as nn
import torch.nn.functional as F

class TrafficCNN(nn.Module):
    def __init__(self):
        super(TrafficCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, stride=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.flatten_dim = 6*6*32
        self.fc1 = nn.Linear(self.flatten_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)  # Nhị phân

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # (16, 15, 15)
        x = self.pool(F.relu(self.conv2(x)))  # (32, 6, 6)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class ClassiEr:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = TrafficCNN()
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def classify(self, imgs):
        images_tensor = torch.tensor(imgs.transpose(0, 3, 1, 2)).float() / 255.0  # [N, 1, 32, 32]
        images_tensor = images_tensor.to(self.device)
        with torch.no_grad():
            outputs = self.model(images_tensor)
            probs = torch.sigmoid(outputs).squeeze(1)
            preds = (probs > 0.5).int()
        return [(pred.item(), prob.item()) for pred, prob in zip(preds, probs)]