from autoplayer import AutoPlayer1
from neural_network import ComplexNN

from pygame_pong import *
from pygame_pong import PygameScreen
from training import NNPlayer

if __name__ == "__main__":

    top_player = NNPlayer(ComplexNN.load("large.model"))
    bottom_player = BottomPygamePlayer()
    screen = PygameScreen(300,550, 60)
    game = Game(screen, top_player, bottom_player)
    game.start_n_games(5)