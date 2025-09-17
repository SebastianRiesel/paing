import json

from autoplayer import AutoPlayer1

from pygame_pong import *
from pygame_pong import PygameScreen
from pytorchnn import PyTorchNN
from training import NNPlayer

if __name__ == "__main__":

    top_player = NNPlayer(PyTorchNN.load())
    #bottom_player = SmallNNPlayer(SmallNN.load_str(json.dumps({"weights": [
    #    [0.7942753618540666, 0.03655633793127767, -0.8334638360436024, -0.6319252674496453, -1.6542692900251246,
    #     0.3617176840827041]], "biases": [0.3928940971375572]})))

    #bottom_player = SmallNNPlayer(SmallNN.load_str(json.dumps({"weights": [
     #  [0.7942753618540666, -0.5, -0.8334638360436024, 0, -1.6542692900251246,
      #   0]], "biases": [0.3928940971375572]})))

    bottom_player = AutoPlayer1()
    screen = PygameScreen(300,550)
    game = Game(screen, top_player, bottom_player)
    game.start_n_games(5, 2000)