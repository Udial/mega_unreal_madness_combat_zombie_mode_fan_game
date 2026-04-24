import pygame


class CollisionSystem:
    def __init__(self): #НЕ ЗАБЫТЬ ДОБАВИТЬ ТУПЛ КОРДОВ ВСЕХ СТЕН В АРГУМЕНТЫ
        self.left_wall_cords = ((200, 980), (0, 1080))
        #self.right_wall_cords =
        #self.top_wall_cords =
        #self.down_wall_cords =

    def get_player_feet_points(self, rect: pygame.Rect) -> list:
        return [rect.bottomleft,
        (rect.centerx, rect.bottom),
        rect.bottomright
        ]
    
    def is_player_point_past_line_horizontal(self, player_feet_point: tuple) -> bool:
        A = self.left_wall_cords[0] 
        B = self.left_wall_cords[1]

        ABx = B[0] - A[0]
        ABy = B[1] - A[1]

        APx = player_feet_point[0] - A[0]
        APy = player_feet_point[1] - A[1]

        cross = ABx * APy - ABy * APx
        return cross > 0
    
    def check_if_player_point_is_beyond_wall(self, player_rect: pygame.Rect) -> bool:
        for point in self.get_player_feet_points(player_rect):
            if self.is_player_point_past_line_horizontal(point):
                return True
        return False