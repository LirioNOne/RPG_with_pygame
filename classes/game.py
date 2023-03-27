import pygame
import sys
from utils import config
from classes.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.level.game_over:
                    self.level.game_end()
            self.screen.fill(config.BG_COLOR)
            self.level.update()
            pygame.display.update()
            self.clock.tick(config.FPS)
