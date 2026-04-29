import pygame
from .base_entity import BaseEntity
from ...settings import BULLET_YELLOW

class Bullet(BaseEntity):
    def __init__(self, x, y, direction, damage):
        super().__init__(x, y, 10, 5)
        
        self.direction = direction
        self.speed = 600
        self.damage = damage
    
    def update(self, dt):
        self.pos_x += self.direction.x * self.speed * dt
        self.pos_y +=  self.direction.y * self.speed * dt
        self.update_rect()

    def render(self, screen):
        pygame.draw.rect(screen, BULLET_YELLOW, self.rect)