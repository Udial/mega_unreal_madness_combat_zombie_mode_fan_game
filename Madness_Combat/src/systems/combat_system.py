import pygame
from ..entities.bullet import Bullet
from ..entities.player import Player
from .economy_manager import EconomyManager
from .input_system import InputState
from .damage_system import DamageSystem


class CombatSystem:
    def __init__(self, entitities: list, player: Player, economy_manager: EconomyManager):
        self.entities = entitities
        self.player = player
        self.economy_manager = economy_manager

    def handle_player_shoot(self, input_state: InputState):
        weapon = self.player.weapon

        if input_state.shoot and weapon.can_shoot():
            weapon.shoot()

            direction = self.get_direction()

            bullet = Bullet(
                self.player.rect.centerx,
                self.player.rect.centery,
                direction,
                weapon.damage
            )

            self.entities.append(bullet)

    def get_direction(self):
        mos_pos = pygame.mouse.get_pos()

        direction = pygame.Vector2(
            mos_pos[0] - self.player.rect.centerx,
            mos_pos[1] - self.player.rect.centery
            )
        
        if direction.length() > 0:
            direction = direction.normalize()

        return direction
    
    def process_bullets(self, bullets: list, zombies: list, damage_system: DamageSystem):
        for bullet in bullets:
            for zombie in zombies:
                if bullet.rect.colliderect(zombie.rect):
                    damage_system.apply_damage(zombie, bullet.damage, self.economy_manager)
                    bullet.is_alive = False