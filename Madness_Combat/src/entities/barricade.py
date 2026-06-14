from .base_entity import BaseEntity
import pygame
from ...settings import WOOD_COLOR, GREEN

class Barricade(BaseEntity):
    def __init__(self, entry_point):
        x, y = entry_point.points[0]
        width, height = entry_point.width, 50

        super().__init__(x, y, width, height)
        self.hp = 50
        self.max_hp = self.hp
        self.level = 1
        self.entry_point = entry_point


    def render(self, screen, camera=None):
        rect = self.rect
        if camera is not None:
            rect = camera.apply(self.rect)
        pygame.draw.rect(screen, WOOD_COLOR, rect)

        