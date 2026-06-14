import pygame
from .base_entity import BaseEntity
from .player import Player
from ...settings import HITBOX_HEIGHT, HITBOX_WIDTH, ZOMBIE_HEALTH, ZOMBIE_SPEED, ZOMBIE_GREEN


class Zombie(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, HITBOX_WIDTH, HITBOX_HEIGHT)
        self.speed = ZOMBIE_SPEED
        self.hp = ZOMBIE_HEALTH
        self.reward = 10
        self.weapon = None
        self.look_direction = pygame.Vector2(0, 0)

    def update_direction(self, player: Player):
        player_pos = pygame.Vector2(player.rect.center)
        zombie_pos = pygame.Vector2(self.rect.center)
        direction = (player_pos - zombie_pos)

        if direction.length() > 0:
            direction = direction.normalize()
        
        self.look_direction = direction
    
    def get_direction(self):
        return self.look_direction

    def render(self, screen, camera=None):
        rect = self.rect
        if camera is not None:
            rect = camera.apply(self.rect)

        pygame.draw.rect(screen, ZOMBIE_GREEN, rect)