import pygame
from pong import *


class PygameScreen(Screen):

    def __init__(self, width, height, fps):
        super().__init__(width, height)
        self.canvas = None
        self.background = (0,0,0)
        self.color = (255,255,255)
        self.fps = fps
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.canvas = pygame.display.set_mode((self.size.x, self.size.y))

    def draw(self, screen_info:ScreenInformation):
        pygame.draw.rect(self.canvas, self.background, pygame.Rect(0, 0, self.size.x, self.size.y))
        pygame.draw.rect(self.canvas, self.color, pygame.Rect(screen_info.top_paddle.x-screen_info.top_paddle.width/2, 0, screen_info.top_paddle.width, screen_info.top_paddle.height))
        pygame.draw.rect(self.canvas, self.color, pygame.Rect(screen_info.bottom_paddle.x-screen_info.bottom_paddle.width/2, self.size.y-screen_info.top_paddle.height, screen_info.top_paddle.width, screen_info.top_paddle.height))

        pygame.draw.rect(self.canvas, self.color, pygame.Rect(screen_info.ball.position.x-screen_info.ball.size.x/2, screen_info.ball.position.y-screen_info.ball.size.y/2, screen_info.ball.size.x, screen_info.ball.size.y))

        top_wins_text = self.font.render(str(screen_info.top_wins),True, self.color)
        bottom_wins_text = self.font.render(str(screen_info.bottom_wins), True, self.color)

        self.canvas.blit(top_wins_text, (10,10))
        self.canvas.blit(bottom_wins_text, (10, self.size.y-40))

        pygame.display.flip()
        self.clock.tick(self.fps)


class BottomPygamePlayer(Player):
    def __init__(self):
        super().__init__()

    def start_game(self):
        pass

    def get_action(self,player_info: PlayerInformation) -> PlayerAction:
        action = PlayerAction.DO_NOTHING

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return PlayerAction.QUIT

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            action = PlayerAction.ACCELERATE_RIGHT
        elif pressed[pygame.K_d]:
            if action == PlayerAction.ACCELERATE_RIGHT:
                action = PlayerAction.DO_NOTHING
            else:
                action = PlayerAction.ACCELERATE_LEFT
        return action

    def end_game(self):
        pass

class TopPygamePlayer(Player):
    def __init__(self):
        super().__init__()

    def start_game(self):
        pass

    def get_action(self,player_info: PlayerInformation) -> PlayerAction:
        action = PlayerAction.DO_NOTHING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return PlayerAction.QUIT
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            action = PlayerAction.ACCELERATE_RIGHT
        elif pressed[pygame.K_LEFT]:
            if action == PlayerAction.ACCELERATE_RIGHT:
                action = PlayerAction.DO_NOTHING
            else:
                action = PlayerAction.ACCELERATE_LEFT
        return action

    def end_game(self):
        pass