import pygame
from ... import settings


class Wall:
    def __init__(self, cords_tuple: tuple, is_collideable: bool):
        self.points = [cords_tuple[0], cords_tuple[1], cords_tuple[2], cords_tuple[3]]
        self.is_collideable = is_collideable
        self.collision_line = (cords_tuple[2], cords_tuple[3])

    def render(self, screen, color, camera=None):
        points = self.points

        if camera is not None:
            points = camera.apply_points(self.points)

        pygame.draw.polygon(screen, color, points, 0)
        pygame.draw.polygon(screen, settings.BLACK, points, 3)
