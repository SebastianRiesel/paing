from abc import abstractclassmethod, abstractmethod, ABC
from collections.abc import Callable
from copy import deepcopy

from autoplayer import AutoPlayer1
from neural_network import NeuralNetwork
from pong import *
from pytorchnn import PyTorchNN
from smallnn import SmallNN


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
    def save(self):
        pass
    @abstractmethod
    def load(self):
        pass

class NNPlayer(TrainablePlayer):
    def load(self):
        pass

    def save(self):
       self.nn.save()

    def __init__(self, nn:NeuralNetwork):
        super().__init__()
        self.nn = nn

    def get_action(self, player_info: PlayerInformation) -> PlayerAction:
        inputs = [player_info.paddle_x/10, player_info.paddle_speed_x/10, player_info.ball_position.x/10,
                  player_info.ball_position.y/10, player_info.ball_speed.x/10, player_info.ball_speed.y/10]
        output = self.nn.think(inputs)[0]

        if output > 1:
            return PlayerAction.ACCELERATE_LEFT
        elif output < -1:
            return PlayerAction.ACCELERATE_RIGHT
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


class EvolutionalTrainer:
    def __init__(self,screen:Screen, ai_generator: Callable[[], TrainablePlayer], ai_count):
        self.screen = screen
        self.ais = []
        for i in range(ai_count):
            self.ais.append(ai_generator())


    def training_iteration(self, play_games_func: Callable[[Screen,list[TrainablePlayer]],[]]):
        for ai in self.ais:
            ai.score = 0

        play_games_func(self.screen, self.ais)

        self.ais.sort(key=lambda ai : ai.score, reverse=True)
        n = 3

        for i in range(n,len(self.ais)):
            self.ais[i] = deepcopy(self.ais[i % n]) # copy the first n ais into all spots
            self.ais[i].mutate(10/i)


def against_each_other(screen:Screen,ais:list[TrainablePlayer]):
    for i in range(len(ais)):
        for j in range(i + 1, len(ais)):
            top = ais[i]
            bottom = ais[j]
            game = Game(screen, top, bottom)
            game.start_n_games(5, 2000)

def against_auto_player(screen:Screen, ais:list[TrainablePlayer]):
    auto = AutoPlayer1()
    for ai in ais:
        game = Game(screen, auto, ai)
        game.start_n_games(5, 2000)

        game = Game(screen, ai, auto)
        game.start_n_games(5, 2000)



if __name__ == "__main__":
    trainer = EvolutionalTrainer(Screen(300,550), lambda : NNPlayer(PyTorchNN()), 10)
    n = 50
    for i in range(n):
        trainer.training_iteration(against_each_other)
        print(f"Score {i+1}/{n}:", trainer.ais[0].score)
        print(trainer.ais[0].nn.state_dict())

    trainer.ais[0].save()


