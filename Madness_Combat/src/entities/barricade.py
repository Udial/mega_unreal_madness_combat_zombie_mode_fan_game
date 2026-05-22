from .base_entity import BaseEntity
import pygame
from ...settings import WOOD_COLOR, GREEN

class Barricade(BaseEntity):
    def __init__(self, entry_point):
        x, y = entry_point.x_topleft, entry_point.y_topleft
        width, height = entry_point.width, 50

        super().__init__(x, y, width, height)
        self.hp = 50
        self.max_hp = self.hp
        self.level = 1
        self.entry_point = entry_point


    def render(self, screen):
        pygame.draw.rect(screen, WOOD_COLOR, self.rect)

        health_bar_width = self.rect.width
        health_bar_height = 6

        health_ratio = self.hp / self.max_hp

        health_rect = pygame.Rect(self.pos_x, self.pos_y - 10, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, GREEN, health_rect)