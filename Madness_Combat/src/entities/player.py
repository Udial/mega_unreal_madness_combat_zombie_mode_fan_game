import pygame
from ..entities.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, hp: int):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.max_hp = 100
        self.hp = hp
        self.max_armor = 100
        self.armor = 0
        self.weapon = None
        self.amount_of_barricades = 0
        self.ammo = 48

    def get_direction(self, camera=None):
        mos_pos = pygame.mouse.get_pos()

        if camera is not None:
            mos_pos = camera.screen_to_world(mos_pos)

        direction = pygame.Vector2(
            mos_pos[0] - self.rect.centerx, mos_pos[1] - self.rect.centery
        )

        if direction.length() > 0:
            direction = direction.normalize()

        return direction

    def render(self, screen: pygame.surface, color: tuple, camera=None):
        rect = self.rect

        if camera is not None:
            rect = camera.apply(self.rect)

        pygame.draw.rect(screen, color, rect)
