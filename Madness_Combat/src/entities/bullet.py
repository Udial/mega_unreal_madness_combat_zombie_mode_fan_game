import math
import pygame
from .base_entity import BaseEntity
from ... import settings


class Bullet(BaseEntity):
    def __init__(self, x, y, direction, damage, speed, pierce=0, sprite_path=None):
        super().__init__(x, y, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
        self.position = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(direction)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.speed = speed
        self.damage = damage
        self.pierce_remaining = max(0, int(pierce))
        self.hit_targets = set()
        self.sprite_path = sprite_path or settings.BULLET_SPRITE_PATH
        self.original_sprite = self._load_sprite()
        self.sprite = self._rotate_to_direction(self.original_sprite)
        self.rect = self.sprite.get_rect(center=(x, y))

    def _load_sprite(self):
        try:
            sprite = pygame.image.load(self.sprite_path).convert_alpha()
            return pygame.transform.scale(
                sprite, (settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
            )
        except Exception:
            surf = pygame.Surface(
                (settings.BULLET_WIDTH, settings.BULLET_HEIGHT), pygame.SRCALPHA
            )
            pygame.draw.ellipse(surf, settings.BULLET_YELLOW, surf.get_rect())
            return surf

    def _rotate_to_direction(self, sprite):
        angle = -math.degrees(math.atan2(self.direction.y, self.direction.x))
        return pygame.transform.rotate(sprite, angle)

    def register_hit(self, target) -> bool:
        target_id = id(target)
        if target_id in self.hit_targets:
            return False
        self.hit_targets.add(target_id)
        if self.pierce_remaining <= 0:
            self.is_alive = False
        else:
            self.pierce_remaining -= 1
        return True

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.pos_x = self.position.x
        self.pos_y = self.position.y
        self.rect.center = (round(self.position.x), round(self.position.y))

    def render(self, screen, camera=None):
        rect = self.rect
        if camera is not None:
            rect = camera.apply(self.rect)
        screen.blit(self.sprite, rect)
