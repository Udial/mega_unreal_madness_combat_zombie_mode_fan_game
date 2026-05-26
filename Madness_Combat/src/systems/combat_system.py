import pygame
from ..entities.bullet import Bullet
from ..entities.player import Player
from .economy_manager import EconomyManager
from .damage_system import DamageSystem
from ..entities.zombie import Zombie
from ..entities.bullet import Bullet
from .input_system import InputState


class CombatSystem:
    def __init__(self, player: Player, economy_manager: EconomyManager, damage_system: DamageSystem, zombie_list: list[Zombie], proj_list: list[Bullet]):
        self.player = player
        self.economy_manager = economy_manager
        self.damage_system = damage_system
        self.zombie_list = zombie_list
        self.proj_list = proj_list

    def attack(self, input_state: InputState):
        if input_state.shoot and self.player.weapon.can_shoot():
            self.player.weapon.shoot()

    def spawn_bullet(self, damage: int):

        direction = self.get_direction()

        bullet = Bullet(
            self.player.rect.centerx,
            self.player.rect.centery,
            direction,
            damage
        )

        self.proj_list.append(bullet)

    def get_direction(self):
        mos_pos = pygame.mouse.get_pos()

        direction = pygame.Vector2(
            mos_pos[0] - self.player.rect.centerx,
            mos_pos[1] - self.player.rect.centery
            )
        
        if direction.length() > 0:
            direction = direction.normalize()

        return direction
    
    def process_bullets(self):
        for bullet in self.proj_list:
            for zombie in self.zombie_list:
                if bullet.rect.colliderect(zombie.rect):
                    self.damage_system.apply_damage(zombie, bullet.damage, self.economy_manager)
                    bullet.is_alive = False

    def process_melee_attack(self, range: int, damage:int):
        dirrection = -self.get_direction()

        player_center = pygame.Vector2(self.player.rect.center)
        offset_disstance = range
        attack_pos = player_center - dirrection * offset_disstance
        attack_size = 60
        attack_rect = pygame.Rect(
            attack_pos.x - attack_size // 2,
            attack_pos.y - attack_size // 2,
            attack_size,
            attack_size
        )

        for zombie in self.zombie_list:
            if zombie.rect.colliderect(attack_rect):
                self.damage_system.apply_damage(zombie, damage, self.economy_manager)
        
        print("DEBUG Attacking using melee")