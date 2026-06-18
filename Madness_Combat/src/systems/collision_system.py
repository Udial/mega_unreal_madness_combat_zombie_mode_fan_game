import pygame
from ...settings import WALL_CORDS_TUPLE, WORLD_WIDTH_MID, WORLD_HEIGHT
from ..entities.wall import Wall


class CollisionSystem:
    def __init__(self, arena_walls_list: list[Wall], shop_walls_list: list[Wall]):
        self.left_wall_cords = (arena_walls_list[0].points[2], arena_walls_list[0].points[3])
        self.right_wall_cords = (arena_walls_list[1].points[2], arena_walls_list[1].points[3])
        self.top_wall_cords = (arena_walls_list[2].points[2], arena_walls_list[2].points[3])

        self.shop_left_wall_cords = (shop_walls_list[0].points[2], shop_walls_list[0].points[3])
        self.shop_right_wall_cords = (shop_walls_list[1].points[2], shop_walls_list[1].points[3])
        self.shop_top_wall_cords = (shop_walls_list[2].points[2], shop_walls_list[2].points[3])

    def get_player_feet_points(self, rect: pygame.Rect) -> list:
        return [rect.bottomleft,
        (rect.centerx, rect.bottom),
        rect.bottomright
        ]
    
    def get_head_pos(self, rect: pygame.Rect):
        return [rect.topleft,
        (rect.centerx, rect.top),
        rect.topright
        ]

    def is_player_point_past_line_horizontal(self, player_feet_point: tuple, room_type: str) -> bool:
        if player_feet_point[0] < WORLD_WIDTH_MID:
            A = self.left_wall_cords[0] if room_type == "arena" else self.shop_left_wall_cords[0]
            B = self.left_wall_cords[1] if room_type == "arena" else self.shop_left_wall_cords[1]

            ABx = B[0] - A[0]
            ABy = B[1] - A[1]

            APx = player_feet_point[0] - A[0]
            APy = player_feet_point[1] - A[1]

            cross = ABx * APy - ABy * APx
            return cross > 0
        else:
            A = self.right_wall_cords[0] if room_type == "arena" else self.shop_right_wall_cords[0]
            B = self.right_wall_cords[1] if room_type == "arena" else self.shop_right_wall_cords[1]

            ABx = A[0] - B[0]
            ABy = A[1] - B[1]

            APx = player_feet_point[0] - B[0]
            APy = player_feet_point[1] - B[1]

            cross = ABx * APy - ABy * APx
            return cross < 0

    def is_player_point_past_line_vertical(self, player_feet_point: tuple) -> bool:
        if self.top_wall_cords[0][1] > player_feet_point[1]:
            return True
        elif player_feet_point[1] > WORLD_HEIGHT:
            return True
        

    def check_if_player_point_is_beyond_wall_horizontal(self, player_rect: pygame.Rect, room_type: str) -> bool:
        for point in self.get_player_feet_points(player_rect):
            if self.is_player_point_past_line_horizontal(point, room_type):
                return True
        return False
    
    def check_if_player_point_is_beyond_wall_vertical(self, player_rect: pygame.Rect) -> bool:
        for point in self.get_player_feet_points(player_rect):
            if self.is_player_point_past_line_vertical(point):
                return True
        return False