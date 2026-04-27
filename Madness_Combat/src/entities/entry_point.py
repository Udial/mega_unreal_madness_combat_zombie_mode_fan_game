import pygame
from .base_entity import BaseEntity
from ...settings import BLACK


class EntryPoint(BaseEntity):
    def __init__(self, x: int, y: int, width: int, height: int, entry_type: str):
        super().__init__(x, y, width, height)
        self.type = entry_type
        self.is_blocked = False
        self.spawn_point = self.rect.center

    def is_open(self):
        return not self.is_blocked
    
    def place_barricade(self, barricade):
        self.barricade = barricade
        self.is_blocked = True

    def remove_barricade(self):
        self.barricade = None
        self.is_blocked = False

    def get_spawn_point(self):
        return self.spawn_point
    
    def render(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)