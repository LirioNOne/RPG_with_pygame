import pygame
from utils import config


class UI:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.hp_bar_rect = pygame.Rect(10, 10, config.HEALTH_BAR_WIDTH, config.HEALTH_BAR_HEIGHT)

    def show(self, current_hp, max_hp, bg_rect, color):
        pygame.draw.rect(self.screen, config.BLACK, bg_rect)

        ratio = current_hp / max_hp
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.screen, color, current_rect)
        pygame.draw.rect(self.screen, config.UI_BORDER, bg_rect, 3)

    def display(self, player):
        self.show(player.health, player.stats['health'], self.hp_bar_rect, config.RED)
