import pygame
from .base_entity import BaseEntity
from ...settings import HITBOX_HEIGHT, HITBOX_WIDTH, ZOMBIE_HEALTH, ZOMBIE_SPEED, ZOMBIE_GREEN


class Zombie(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, HITBOX_WIDTH, HITBOX_HEIGHT)
        self.speed = ZOMBIE_SPEED
        self.hp = ZOMBIE_HEALTH

    def render(self, screen):
        pygame.draw.rect(screen, ZOMBIE_GREEN, self.rect)