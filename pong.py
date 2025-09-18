from enum import Enum
from random import random, randint

from vector import Vector2

def flip_position( pos, max_pos):
    return max_pos - pos


class PlayerInformation:
    def __init__(self, paddle, opponent_paddle, ball, screen):
        if paddle.side == PaddleSide.BOTTOM:
            self.paddle_x = flip_position(paddle.x, screen.size.x)
            self.paddle_speed_x = -paddle.speed_x
            self.opponent_x = flip_position(opponent_paddle.x, screen.size.x)
            self.opponent_speed_x = -opponent_paddle.speed_x
            self.ball_position = flip_position(ball.position, screen.size)
            self.ball_speed = -ball.direction.normalized().scaled(ball.speed)
        else:
            self.paddle_x = paddle.x
            self.paddle_speed_x = paddle.speed_x
            self.opponent_x = opponent_paddle.x
            self.opponent_speed_x = opponent_paddle.speed_x
            self.ball_position = ball.position
            self.ball_speed = ball.direction.normalized().scaled(ball.speed)

        self.screen_size = screen.size


class PlayerAction(Enum):
    ACCELERATE_LEFT = 1
    ACCELERATE_RIGHT = 2
    DO_NOTHING = 3
    QUIT = 4

class ScreenInformation:
    def __init__(self, top_paddle, bottom_paddle, ball, top_wins, bottom_wins):
        self.top_paddle = top_paddle
        self.bottom_paddle = bottom_paddle
        self.ball = ball
        self.top_wins = top_wins
        self.bottom_wins = bottom_wins

class GameData:
    def __init__(self):
        self.ball_paddle_distances = []
        self.hits = 0
        self.misses = 0
        self.losses = 0
        self.wins = 0
        self.draws = 0

    def __str__(self):
        return f'GameData[Wins:{self.wins}, Losses:{self.losses}, Draws:{self.draws}, Ball Paddle Distances:{self.ball_paddle_distances}]'


class Screen:
    def __init__(self, width, height):
        self.size = Vector2(width, height)

    def start_game(self):
        pass

    def draw(self, screen_info:ScreenInformation):
        pass

    def end_game(self):
        pass

class Player:
    def __init__(self):
        pass

    def get_action(self,player_info: PlayerInformation) -> PlayerAction:
        return PlayerAction.DO_NOTHING


    def receive_player_data(self, data: GameData):
        pass



class PaddleSide(Enum):
    TOP=0 # top of the screen, aka y nearly 0
    BOTTOM=1 # bottom of the screen, aka x nearly screen_height

class Paddle:
    def __init__(self,x, side):
        self.speed_x = 0 # current speed of the paddle
        self.x = x # current center position of the paddle
        self.side = side # is the paddle on the top or the bottom?
        self.height = 10
        self.width = 60
        self.acceleration = 0.1

    # accelerate either to left (direction=-1) or right direction=1
    def accelerate(self, direction):
        self.speed_x += self.acceleration*direction

    def move(self):
        self.x += self.speed_x

    def reverse(self):
        self.speed_x = -self.speed_x

    def ball_hits_paddle(self,screen_height, ball):
        x_inside = (self.x + self.width / 2) > ball.position.x > (self.x - self.width / 2)

        if self.side == PaddleSide.BOTTOM:
            y_inside = screen_height > ball.position.y > screen_height - self.height
        else:
            y_inside = 0 < ball.position.y < self.height

        return x_inside and y_inside



class Ball:
    def __init__(self, position:Vector2):
        self.position = position
        self.direction = Vector2(3,1.5) # direction of movement
        self.speed = 3 # speed of movement
        self.size = Vector2(10,10)
        self.acceleration = 0.1
        self.max_speed = 6

    def reverse_x(self):
        self.direction.x = -self.direction.x

    def reverse_y(self):
        self.direction.y = -self.direction.y

    def move(self):
        self.position += self.direction.normalized().scaled(self.speed)

    def accelerate(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration



class Game:
    def __init__(self, screen:Screen, top_player:Player, bottom_player:Player):
        self.screen = screen
        self.top_player = top_player
        self.bottom_player = bottom_player

        self.ball = Ball(screen.size.scaled(0.5))

        self.top_paddle = Paddle(screen.size.x/2,PaddleSide.TOP)
        self.bottom_paddle = Paddle(screen.size.x/2,PaddleSide.BOTTOM)
        self.running = False

        self.top_game_data = GameData()
        self.bottom_game_data = GameData()

    def do_actions(self):
        top_info = PlayerInformation(self.top_paddle,self.bottom_paddle, self.ball, self.screen)
        bottom_info = PlayerInformation(self.bottom_paddle,self.top_paddle, self.ball, self.screen)

        top_action = self.top_player.get_action(top_info)
        bottom_action = self.bottom_player.get_action(bottom_info)

        if bottom_action == PlayerAction.ACCELERATE_LEFT:
            self.bottom_paddle.accelerate(1)
        elif bottom_action == PlayerAction.ACCELERATE_RIGHT:
            self.bottom_paddle.accelerate(-1)
        elif bottom_action == PlayerAction.QUIT:
            self.running = False
        if top_action == PlayerAction.ACCELERATE_LEFT:
            self.top_paddle.accelerate(-1)
        elif top_action == PlayerAction.ACCELERATE_RIGHT:
            self.top_paddle.accelerate(1)
        elif top_action == PlayerAction.QUIT:
            self.running = False



    def handle_physics(self):
        # physics
        if self.ball.position.x < 0 or self.ball.position.x > self.screen.size.x:
            self.ball.reverse_x()

        if self.bottom_paddle.ball_hits_paddle(self.screen.size.y, self.ball):
            self.bottom_game_data.ball_paddle_distances.append(self.bottom_paddle.x - self.ball.position.x)
            self.bottom_game_data.hits +=1
            self.ball.position.y = self.screen.size.y - self.bottom_paddle.height - self.ball.size.y/2
            self.ball.direction = self.ball.position - Vector2(self.bottom_paddle.x, self.screen.size.y)
            self.ball.accelerate()


        if self.top_paddle.ball_hits_paddle(self.screen.size.y, self.ball):
            self.top_game_data.ball_paddle_distances.append(self.ball.position.x - self.top_paddle.x)
            self.top_game_data.hits += 1
            self.ball.position.y = self.top_paddle.height + self.ball.size.y / 2
            self.ball.direction = self.ball.position - Vector2(self.top_paddle.x, 0)
            self.ball.accelerate()

        if self.ball.position.y < 0:
            self.top_game_data.ball_paddle_distances.append(self.ball.position.x - self.top_paddle.x)
            self.top_game_data.misses += 1
            self.top_game_data.losses += 1
            self.bottom_game_data.wins += 1
            self.running = False

        if self.ball.position.y > self.screen.size.y:
            self.bottom_game_data.ball_paddle_distances.append(self.bottom_paddle.x - self.ball.position.x)
            self.bottom_game_data.misses += 1
            self.bottom_game_data.losses += 1
            self.top_game_data.wins += 1
            self.running = False

        if self.top_paddle.x + self.top_paddle.width / 2 > self.screen.size.x:
            self.top_paddle.reverse()
            self.top_paddle.speed_x *= 0.8
            self.top_paddle.x = self.screen.size.x - self.top_paddle.width / 2

        if self.top_paddle.x - self.top_paddle.width / 2 < 0:
            self.top_paddle.reverse()
            self.top_paddle.speed_x *= 0.8
            self.top_paddle.x = self.top_paddle.width / 2

        if self.bottom_paddle.x + self.bottom_paddle.width / 2 > self.screen.size.x:
            self.bottom_paddle.reverse()
            self.bottom_paddle.speed_x *= 0.8
            self.bottom_paddle.x = self.screen.size.x - self.bottom_paddle.width / 2

        if self.bottom_paddle.x - self.bottom_paddle.width / 2 < 0:
            self.bottom_paddle.reverse()
            self.bottom_paddle.speed_x *= 0.8
            self.bottom_paddle.x = self.bottom_paddle.width / 2

    def single_game(self, max_frames:int):
        self.ball = Ball(self.screen.size.scaled(0.5))
        self.ball.direction = Vector2(random()*2 - 1, randint(0,1)*2 - 1)

        self.top_paddle = Paddle(self.screen.size.x / 2, PaddleSide.TOP)
        self.bottom_paddle = Paddle(self.screen.size.x / 2, PaddleSide.BOTTOM)

        self.running = True

        self.screen.start_game()

        frames = 0
        while self.running:

            self.do_actions()

            self.bottom_paddle.move()
            self.top_paddle.move()
            self.ball.move()

            self.handle_physics()

            screen_information = ScreenInformation(self.top_paddle, self.bottom_paddle, self.ball, self.top_game_data.wins, self.bottom_game_data.wins)
            self.screen.draw(screen_information)

            frames += 1
            if frames > max_frames > 0:
                self.running = False
                self.top_game_data.draws += 1
                self.bottom_game_data.draws += 1


        self.screen.end_game()


    def start_n_games(self, num_games: int, max_frames_per_game:int = -1):
        self.top_game_data = GameData()
        self.bottom_game_data = GameData()
        for i in range(num_games):
            self.single_game(max_frames_per_game)
        self.top_player.receive_player_data(self.top_game_data)
        self.bottom_player.receive_player_data(self.bottom_game_data)




