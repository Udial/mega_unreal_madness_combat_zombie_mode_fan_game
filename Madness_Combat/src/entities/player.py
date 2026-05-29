import pygame
from ..entities.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, x: int, y: int, width: int , height: int, speed: int, hp: int):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.hp = hp
        self.weapon = None
        self.amount_of_barricades = 0
        self.ammo = 200

    def get_direction(self):
        mos_pos = pygame.mouse.get_pos()

        direction = pygame.Vector2(
            mos_pos[0] - self.rect.centerx,
            mos_pos[1] - self.rect.centery
            )
        
        if direction.length() > 0:
            direction = direction.normalize()

        return direction
    
    def render(self, screen: pygame.surface, color: tuple, rect: pygame.Rect):
        pygame.draw.rect(screen, color, rect)
