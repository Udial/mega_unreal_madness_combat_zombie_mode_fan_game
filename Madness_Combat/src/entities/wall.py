import pygame
from ... import settings


class Wall():
    def __init__(self, cords_tuple: tuple, is_collideable: bool):
        self.x_topleft, self.y_topleft = cords_tuple[0]
        self.x_topright, self.y_topright = cords_tuple[1]
        self.x_downrigth, self.y_downright = cords_tuple[2]
        self.x_downleft, self.y_downleft = cords_tuple[3]
        self.is_collideable = is_collideable
        self.collision_line = (cords_tuple[2],cords_tuple[3])

    def render(self, screen, color):
        pygame.draw.polygon(screen, color, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 0)
        pygame.draw.polygon(screen, settings.BLACK, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 3)