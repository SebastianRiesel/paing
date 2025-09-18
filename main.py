from autoplayer import AutoPlayer1
from complexnn import ComplexNNLayer, ComplexNN

from pygame_pong import *
from pygame_pong import PygameScreen
from pytorchnn import PyTorchNN
from training import NNPlayer

if __name__ == "__main__":

    top_player = NNPlayer(ComplexNN.load("simple.model"))
    bottom_player = AutoPlayer1()
    screen = PygameScreen(300,550, 60)
    game = Game(screen, top_player, bottom_player)
    game.start_n_games(5, 2000)