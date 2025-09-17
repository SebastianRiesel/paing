import json
from random import random

from neural_network import NeuralNetwork

def activation(x):
    return x


class SmallNN(NeuralNetwork):
    def save(self):
        pass

    @staticmethod
    def load():
        pass

    def __init__(self, in_nodes: int, out_nodes: int, random_range:float):
        super().__init__()
        self.data = {"weights":[], "biases":[]}


        for i in range(out_nodes):
            self.data["weights"].append([])
            self.data["biases"].append(random() * random_range - random_range/2)
            for j in range(in_nodes):
                self.data["weights"][i].append(random() * random_range - random_range/2)

    def mutate(self, random_range:float):
        for i in range(len(self.data["weights"])):
            self.data["biases"][i] += random()*random_range - random_range/2
            for j in range(len(self.data["weights"][i])):
                self.data["weights"][i][j]+=random()*random_range - random_range/2


    def think(self, inputs):
        output = []
        for out_i in range(len(self.data["weights"])):
            assert len(inputs) == len(self.data["weights"][out_i])
            sum_out = 0
            for in_i in range(len(self.data["weights"][out_i])):
                sum_out+=inputs[in_i]*self.data["weights"][out_i][in_i]
            output.append(activation(sum_out) + self.data["biases"][out_i])
        return output



    def dump_str(self) -> str:
        return json.dumps(self.data)

    @staticmethod
    def load_str(string:str):
        data = json.loads(string)
        nn = SmallNN(0,0, 0)
        nn.data = data
        return nn


