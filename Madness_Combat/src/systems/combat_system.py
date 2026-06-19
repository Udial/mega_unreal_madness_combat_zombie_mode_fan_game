import pygame
from random import uniform
from ..entities.bullet import Bullet
from ..entities.player import Player
from .economy_manager import EconomyManager
from .damage_system import DamageSystem
from ..entities.zombie import Zombie
from .input_system import InputState


class CombatSystem:
    def __init__(
        self,
        player: Player,
        economy_manager: EconomyManager,
        damage_system: DamageSystem,
        zombie_list: list[Zombie],
        proj_list: list[Bullet],
        camera=None,
    ):
        self.player = player
        self.economy_manager = economy_manager
        self.damage_system = damage_system
        self.zombie_list = zombie_list
        self.proj_list = proj_list
        self.camera = camera

    def attack(self, input_state: InputState):
        weapon = self.player.weapon
        if weapon is None:
            return
        if getattr(weapon, "fire_mode", "semiauto") == "automatic":
            if input_state.shoot:
                weapon.shoot()
        elif input_state.shoot_pressed:
            weapon.shoot()

    def spawn_bullet(
        self, damage: int, spread: int, speed: int, pierce: int = 0, origin=None
    ):
        direction = self.player.get_direction(self.camera)
        angle = uniform(-spread, spread)
        pellet_direction = direction.rotate(angle)
        if origin is None:
            origin = self.player.rect.center
        bullet = Bullet(origin[0], origin[1], pellet_direction, damage, speed, pierce)
        self.proj_list.append(bullet)

    def process_bullets(self):
        for bullet in list(self.proj_list):
            if not bullet.is_alive:
                continue
            for zombie in list(self.zombie_list):
                if not zombie.is_alive:
                    continue
                if bullet.rect.colliderect(zombie.rect) and bullet.register_hit(zombie):
                    self.damage_system.apply_damage(zombie, bullet.damage)
                    if not bullet.is_alive:
                        break

    def process_melee_attack(self, attack_range: int, damage: int):
        direction = self.player.get_direction(self.camera)
        player_center = pygame.Vector2(self.player.rect.center)
        attack_pos = player_center + direction * attack_range
        attack_size = 60
        attack_rect = pygame.Rect(
            attack_pos.x - attack_size // 2,
            attack_pos.y - attack_size // 2,
            attack_size,
            attack_size,
        )
        for zombie in self.zombie_list:
            if zombie.rect.colliderect(attack_rect):
                self.damage_system.apply_damage(zombie, damage)

    def process_zombie_melee_attack(self, damage):
        self.damage_system.apply_damage(self.player, damage)
