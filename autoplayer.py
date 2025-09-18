from pong import *

class AutoPlayer1(Player):
    def __init__(self):
        super().__init__()

    def get_action(self,player_info: PlayerInformation) -> PlayerAction:
        if player_info.ball_position.x - player_info.paddle_x > 30:
            return PlayerAction.ACCELERATE_RIGHT
        elif player_info.ball_position.x - player_info.paddle_x < -30:
            return PlayerAction.ACCELERATE_LEFT
        else:
            if player_info.paddle_speed_x > player_info.ball_speed.x:
                return PlayerAction.ACCELERATE_LEFT
            elif player_info.paddle_speed_x < player_info.ball_speed.x:
                return PlayerAction.ACCELERATE_RIGHT
            else:
                return PlayerAction.DO_NOTHING

    def receive_player_data(self, data: GameData):
        pass