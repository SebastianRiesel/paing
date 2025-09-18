from abc import ABC, abstractmethod

class NeuralNetwork(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def think(self, inputs):
        pass
    @abstractmethod
    def mutate(self,random_range:float):
        pass

    @abstractmethod
    def save(self, path):
        pass


    @staticmethod
    @abstractmethod
    def load(path):
        pass

import json
from enum import Enum, IntEnum
from random import random

from neural_network import NeuralNetwork


def relu(x):
    return max(0,x)

def linear(x):
    return x

def leaky_relu(x):
    return max(x/5, x)

class ActivationFunction(IntEnum):
    RELU = 0
    LINEAR = 1
    LEAKY_RELU = 2

def call_activation(activation,x):
    match activation:
        case ActivationFunction.RELU:
            return relu(x)
        case ActivationFunction.LEAKY_RELU:
            return leaky_relu(x)
        case ActivationFunction.LINEAR:
            return linear(x)
    raise TypeError(activation)


class ComplexNNLayer:
    def __init__(self, in_count, out_count,activation:ActivationFunction, random_range):
        self.weights = []
        self.biases = []

        self.activation = activation
        for i in range(out_count):
            self.weights.append([])
            self.biases.append(random()*random_range - random_range/2)
            for j in range(in_count):
                self.weights[i].append(random()*random_range - random_range/2)

    def mutate(self, random_range):
        for out_i in range(len(self.weights)):
            self.biases[out_i] += random()*random_range - random_range/2
            for in_i in range(len(self.weights[out_i])):
                self.weights[out_i][in_i] += random() * random_range - random_range / 2

    def forward(self, inputs):
        outs = []
        for out_i in range(len(self.weights)):
            value = 0
            for in_i in range(len(self.weights[out_i])):
                value+=self.weights[out_i][in_i] * inputs[in_i]
            value+=self.biases[out_i]
            value = call_activation(self.activation, value)
            outs.append(value)

        return outs

    def to_dict(self):
        return {
            "activation":self.activation,
            "weights":self.weights,
            "biases":self.biases
        }
    def from_dict(self, data):
        self.activation = data["activation"]
        self.weights = data["weights"]
        self.biases = data["biases"]


class ComplexNN(NeuralNetwork):
    def __init__(self, layers: list[ComplexNNLayer]):
        super().__init__()
        self.layers = layers


    def think(self, inputs):
        next_inputs = inputs
        for layer in self.layers:
            next_inputs = layer.forward(next_inputs)
        return next_inputs


    def mutate(self, random_range: float):
        for layer in self.layers:
            layer.mutate(random_range)

    def save(self, path):
        data = []
        for layer in self.layers:
            data.append(layer.to_dict())
        with open(path, "w+") as file:
            file.write(json.dumps(data))



    @staticmethod
    def load(path):
        content = ""
        with open(path, "r") as file:
            content = file.read()

        data = json.loads(content)

        nn = ComplexNN([])
        for layer_data in data:
            layer = ComplexNNLayer(0,0,0,0)
            layer.from_dict(layer_data)
            nn.layers.append(layer)
        return nn










