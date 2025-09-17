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
    def save(self):
        pass


    @staticmethod
    @abstractmethod
    def load():
        pass









