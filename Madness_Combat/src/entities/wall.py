import pygame
from ... import settings


class Wall():
    def __init__(self, x_topleft: int, y_topleft: int, x_topright: int, y_topright: int, x_downrigth: int, y_downright: int, x_downleft: int, y_downleft: int, is_collideable: bool):
        self.x_topleft = x_topleft
        self.y_topleft = y_topleft
        self.x_topright = x_topright
        self.y_topright = y_topright
        self.x_downrigth = x_downrigth
        self.y_downright = y_downright
        self.x_downleft = x_downleft
        self.y_downleft = y_downleft
        self.is_collideable = is_collideable

    def render(self, screen, color):
        pygame.draw.polygon(screen, color, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 0)
        pygame.draw.polygon(screen, settings.BLACK, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 3)