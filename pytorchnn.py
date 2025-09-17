import torch
from torch import nn

from neural_network import NeuralNetwork

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"

class PyTorchNN(NeuralNetwork, nn.Module):
    def save(self):
        torch.save(self.state_dict(), "pytorch.model")

    @staticmethod
    def load():
        model = PyTorchNN()
        model.load_state_dict(torch.load("pytorch.model", weights_only=True))
        model.eval()
        print(model.state_dict())
        return model

    def __init__(self):
        super(PyTorchNN, self).__init__()
        self.fc1 = nn.Linear(6, 4)
        self.fc2 = nn.Linear(4, 1)


    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def think(self, inputs):
        tensor = torch.tensor(inputs, dtype=torch.float32).view(1,-1)
        return self(tensor)

    def mutate(self, random_range):
        with torch.no_grad():
            for param in self.parameters():
                param.add_(torch.randn_like(param) * random_range)

