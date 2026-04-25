import pygame
from ...settings import WALL_CORDS_TUPLE, SCREEN_WIDTH_MID, SCREEN_HEIGHT


class CollisionSystem:
    def __init__(self):
        self.left_wall_cords = (WALL_CORDS_TUPLE[0][2], WALL_CORDS_TUPLE[0][3])
        self.right_wall_cords = (WALL_CORDS_TUPLE[1][2], WALL_CORDS_TUPLE[1][3])
        self.top_wall_cords = (WALL_CORDS_TUPLE[2][2], WALL_CORDS_TUPLE[2][3])
        #self.down_wall_cords =

    def get_player_feet_points(self, rect: pygame.Rect) -> list:
        return [rect.bottomleft,
        (rect.centerx, rect.bottom),
        rect.bottomright
        ]
    
    def is_player_point_past_line_horizontal(self, player_feet_point: tuple) -> bool:
        if player_feet_point[0] < SCREEN_WIDTH_MID:
            A = self.left_wall_cords[0] 
            B = self.left_wall_cords[1]

            ABx = B[0] - A[0]
            ABy = B[1] - A[1]

            APx = player_feet_point[0] - A[0]
            APy = player_feet_point[1] - A[1]

            cross = ABx * APy - ABy * APx
            return cross > 0
        else:
            A = self.right_wall_cords[0] 
            B = self.right_wall_cords[1]

            ABx = A[0] - B[0]
            ABy = A[1] - B[1]

            APx = player_feet_point[0] - B[0]
            APy = player_feet_point[1] - B[1]

            cross = ABx * APy - ABy * APx
            return cross < 0

    def is_player_point_past_line_vertical(self, player_feet_point: tuple) -> bool:
        if self.top_wall_cords[0][1] > player_feet_point[1]:
            return True
        elif player_feet_point[1] > SCREEN_HEIGHT:
            return True
        

    def check_if_player_point_is_beyond_wall_horizontal(self, player_rect: pygame.Rect) -> bool:
        for point in self.get_player_feet_points(player_rect):
            if self.is_player_point_past_line_horizontal(point):
                return True
        return False
    
    def check_if_player_point_is_beyond_wall_vertical(self, player_rect: pygame.Rect) -> bool:
        for point in self.get_player_feet_points(player_rect):
            if self.is_player_point_past_line_vertical(point):
                return True
        return False