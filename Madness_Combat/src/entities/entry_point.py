import pygame
from .base_entity import BaseEntity
from ...settings import BLACK


class EntryPoint(BaseEntity):
    def __init__(self, cords_tuple: tuple, entry_type: str):
        self.x_topleft, self.y_topleft = cords_tuple[0]
        self.x_topright, self.y_topright = cords_tuple[1]
        self.x_downrigth, self.y_downright = cords_tuple[2]
        self.x_downleft, self.y_downleft = cords_tuple[3]
        width = self.x_topright - self.x_topleft
        height = self.y_downleft - self.y_topleft

        super().__init__(self.x_topleft, self.y_topleft, width, height)
        
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
    
    def render(self, screen, color):
        pygame.draw.polygon(screen, color, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 0)
        pygame.draw.polygon(screen, BLACK, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 2)