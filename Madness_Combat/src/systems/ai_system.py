import pygame
from ..entities.player import Player
from ..entities.zombie import Zombie
from ... import settings


class AISystem:
    def __init__(self, movement_system, player: Player):
        self.movement_system = movement_system
        self.player = player

    def update(self, zombies: list[Zombie], room_type: str, dt):
        for zombie in zombies:
            if zombie.get_distance_to(self.player) <= zombie.weapon.range:
                zombie.weapon.shoot()
                continue
            input_state = self._build_input(zombie, zombies)
            self.movement_system.update(zombie, input_state, room_type, dt)

    def _build_input(self, zombie, zombies):
        seek = pygame.Vector2(
            self.player.rect.centerx - zombie.rect.centerx,
            self.player.rect.centery - zombie.rect.centery,
        )
        if seek.length() > 0:
            seek = seek.normalize()

        separation = pygame.Vector2(0, 0)
        for other in zombies:
            if other is zombie or not other.is_alive:
                continue
            offset = pygame.Vector2(zombie.rect.center) - pygame.Vector2(
                other.rect.center
            )
            distance = offset.length()
            if 0 < distance < settings.ZOMBIE_SEPARATION_RADIUS:
                separation += (
                    offset.normalize()
                    * (settings.ZOMBIE_SEPARATION_RADIUS - distance)
                    / settings.ZOMBIE_SEPARATION_RADIUS
                )

        direction = seek + separation * settings.ZOMBIE_SEPARATION_WEIGHT
        if direction.length() > 0:
            direction = direction.normalize()

        class AIInput:
            def __init__(self, move):
                self.move = move
                self.shoot = False

        return AIInput(direction)
