import pygame


class BaseEntity:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.pos_x = x
        self.pos_y = y
        self.position = pygame.Vector2(self.pos_x, self.pos_y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, width, height)

    def update_hitbox(self):
        self.rect.topleft = self.position