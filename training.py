import datetime
from abc import  abstractmethod, ABC
from collections.abc import Callable
from copy import deepcopy

import complexnn
from autoplayer import AutoPlayer1
from neural_network import NeuralNetwork, ComplexNNLayer, ActivationFunction, ComplexNN
from pong import *
from pygame_pong import PygameScreen


# scores have to be larger than zero to work
class TrainablePlayer(Player, ABC):
    def __init__(self):
        super().__init__()
        self.score = 0

    @abstractmethod
    def mutate(self, number_gen:Callable[[], float]):
        pass

    @abstractmethod
    def calculate_score(self, data:GameData) -> float:
        pass

    def receive_player_data(self, data: GameData):
        self.score += self.calculate_score(data)

    @abstractmethod
    def save(self, path):
        pass


class NNPlayer(TrainablePlayer):

    def __init__(self, nn:NeuralNetwork):
        super().__init__()
        self.nn = nn

    def get_action(self, player_info: PlayerInformation) -> PlayerAction:
        inputs = [player_info.paddle_x/100,         player_info.paddle_speed_x/10,
                  player_info.ball_position.x/100,  player_info.ball_position.y/100,
                  player_info.ball_speed.x/10,      player_info.ball_speed.y/10,
                  player_info.opponent_x/100,       player_info.opponent_speed_x/10]
        output = self.nn.think(inputs)

        if output[0] - output [1] < -0.5:
            return PlayerAction.ACCELERATE_RIGHT
        elif output[0] - output [1] > 0.5:
            return PlayerAction.ACCELERATE_LEFT
        else:
            return PlayerAction.DO_NOTHING

    def mutate(self, random_range:float):
        self.nn.mutate(random_range)

    def calculate_score(self, data:GameData) -> float:
        if data.hits + data.misses > 0:
            hit_score = data.hits/(data.hits+data.misses)
        else:
            hit_score = 0
        games = data.wins + data.losses + data.draws
        win_score = data.wins/games

        if len(data.ball_paddle_distances) > 0:
            distance_score = -1 * sum(data.ball_paddle_distances)/len(data.ball_paddle_distances)
        else:
            distance_score = 0

        return hit_score*100  + win_score * 1000 + distance_score

    def save(self, path):
        self.nn.save(path)



class EvolutionalTrainer:
    def __init__(self,screen:Screen, ai_generator: Callable[[], TrainablePlayer], ai_count, stay_alive_count):
        self.screen = screen
        self.stay_alive_count = stay_alive_count
        self.ais = []
        for i in range(ai_count):
            self.ais.append(ai_generator())


    def training_iteration(self, play_games_func: Callable[[Screen,list[TrainablePlayer]],[]]):
        for ai in self.ais:
            ai.score = 0

        play_games_func(self.screen, self.ais)

        self.ais.sort(key=lambda ai_obj : ai_obj.score, reverse=True)

        for i in range(self.stay_alive_count, len(self.ais)):
            self.ais[i] = deepcopy(self.ais[i % self.stay_alive_count]) # copy the first n ais into all spots
            self.ais[i].mutate(0.5)


def against_each_other(screen:Screen,ais:list[TrainablePlayer]):
    for i in range(len(ais)):
        for j in range(i + 1, len(ais)):
            top = ais[i]
            bottom = ais[j]
            game = Game(screen, top, bottom)
            game.start_n_games(3, 2000)



def against_auto_player(screen:Screen, ais:list[TrainablePlayer]):
    auto = AutoPlayer1()
    for ai in ais:
        game = Game(screen, ai, auto)
        game.start_n_games(3, 2500)

        game = Game(screen, auto, ai)
        game.start_n_games(3, 2500)



if __name__ == "__main__":

    layer1 = ComplexNNLayer(8,4,ActivationFunction.RELU, 1)
    layer2 = ComplexNNLayer(4, 4, ActivationFunction.RELU, 1)
    layer3 = ComplexNNLayer(4, 2, ActivationFunction.LINEAR, 1)
    nn = ComplexNN([layer1, layer2, layer3])

    #nn = PyTorchNN()

    trainer = EvolutionalTrainer(Screen(300,550), lambda : NNPlayer(nn), 20, 4)
    n = 500
    for iteration in range(n):
        trainer.training_iteration(against_each_other)
        print(f"Score {iteration + 1}/{n}:", trainer.ais[0].score)

    trainer.ais[0].save(f'large.model')

    top_player = trainer.ais[0]
    bottom_player = AutoPlayer1()
    screen = PygameScreen(300, 550, 60)
    game = Game(screen, top_player, bottom_player)

    while True:
        game.start_n_games(5)
