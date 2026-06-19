import pygame


class BaseEntity:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.pos_x = x
        self.pos_y = y
        self.position = pygame.Vector2(self.pos_x, self.pos_y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, width, height)
        self.is_alive = True

    def update_rect(self):
        self.rect.topleft = (self.pos_x, self.pos_y)

    def get_distance_to(self, target) -> int:
        self_pos = pygame.Vector2(self.rect.center)
        target_pos = pygame.Vector2(target.rect.center)
        return self_pos.distance_to(target_pos)
