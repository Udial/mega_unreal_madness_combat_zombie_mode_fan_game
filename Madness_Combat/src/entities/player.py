import pygame
from ..entities.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, x: int, y: int, width: int , height: int, speed: int, hp: int):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.hp = hp
    
    def render(self, screen: pygame.surface, color: tuple, rect: pygame.Rect):
        pygame.draw.rect(screen, color, rect)