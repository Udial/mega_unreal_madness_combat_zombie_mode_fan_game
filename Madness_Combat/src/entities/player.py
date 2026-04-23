import pygame
from ..entities.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, x: int, y: int, width: int , height: int, speed: int, hp: int):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.hp = hp
        self.prev_pos_x = self.pos_x
        self.prev_pos_y = self.pos_y
    
    def get_feet_points(self, rect: pygame.Rect) -> list:
        return [rect.bottomleft,
        (rect.centerx, rect.bottom),
        rect.bottomright
        ]
    
    def is_point_past_line_horizontal(self, cord_tuple: tuple, player_feet_point: tuple) -> bool:
        ABx = cord_tuple[0][0] - cord_tuple[1][0]
        ABy = cord_tuple[0][1] - cord_tuple[1][1]

        APx = player_feet_point[0] - cord_tuple[0][0]
        APy = player_feet_point[1] - cord_tuple[0][1]

        cross = ABx * APy - ABy * APx

        return cross < 0
    
    def check_if_point_is_beyond_wall(self, cord_tuple: tuple, player_rect: pygame.Rect) -> bool:
        for point in self.get_feet_points(player_rect):
            if self.is_point_past_line_horizontal(cord_tuple, point):
                return True
        return False

    def render(self, screen: pygame.surface, color: tuple, rect: pygame.Rect):
        pygame.draw.rect(screen, color, rect)