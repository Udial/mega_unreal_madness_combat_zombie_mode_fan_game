import pygame
from .base_entity import BaseEntity
from .player import Player
from ...settings import (
    HITBOX_HEIGHT,
    HITBOX_WIDTH,
    ZOMBIE_HEALTH,
    ZOMBIE_SPEED,
    ZOMBIE_GREEN,
    ZOMBIE_HEALTH_BAR_WIDTH,
    ZOMBIE_HEALTH_BAR_HEIGHT,
    ZOMBIE_HEALTH_BAR_OFFSET_Y,
)
from ... import settings


class Zombie(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, HITBOX_WIDTH, HITBOX_HEIGHT)
        self.speed = ZOMBIE_SPEED
        self.max_hp = ZOMBIE_HEALTH
        self.hp = ZOMBIE_HEALTH
        self.armor = 0
        self.reward = 10
        self.weapon = None
        self.look_direction = pygame.Vector2(0, 0)

    def update_direction(self, player: Player):
        player_pos = pygame.Vector2(player.rect.center)
        zombie_pos = pygame.Vector2(self.rect.center)
        direction = player_pos - zombie_pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.look_direction = direction

    def get_direction(self):
        return self.look_direction

    def render_health_bar(self, screen, camera=None):
        hp_ratio = max(0, min(1, self.hp / self.max_hp))
        bar_rect = pygame.Rect(0, 0, ZOMBIE_HEALTH_BAR_WIDTH, ZOMBIE_HEALTH_BAR_HEIGHT)
        bar_rect.centerx = self.rect.centerx
        bar_rect.bottom = self.rect.top - ZOMBIE_HEALTH_BAR_OFFSET_Y
        if camera is not None:
            bar_rect = camera.apply(bar_rect)
        fill_rect = bar_rect.copy()
        fill_rect.width = int(bar_rect.width * hp_ratio)
        pygame.draw.rect(screen, settings.RED, bar_rect)
        pygame.draw.rect(screen, settings.GREEN, fill_rect)
        pygame.draw.rect(screen, settings.BLACK, bar_rect, 1)

    def render(self, screen, camera=None):
        rect = self.rect
        if camera is not None:
            rect = camera.apply(self.rect)
        pygame.draw.rect(screen, ZOMBIE_GREEN, rect)
        self.render_health_bar(screen, camera)
