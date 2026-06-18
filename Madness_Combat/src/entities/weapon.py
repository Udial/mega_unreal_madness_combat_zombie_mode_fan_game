import pygame
import math
from .player import Player
from .zombie import Zombie
from ..systems.combat_system import CombatSystem


class Weapon:
    def __init__(self, data: dict, combat_system: CombatSystem,):
        self.damage = data["damage"]
        self.cooldown = 0
        self.attack_rate = data["fire_rate"]
        self.owner = None
        self.combat_system = combat_system
        self.name = data["name"]
        self.weapon_id = None

        self.sprite_path = data["sprite"]
        self.sprite_widht = data["sprite_width"]
        self.sprite_height = data["sprite_height"]
        self.original_sprite = pygame.image.load(self.sprite_path).convert_alpha()
        self.original_sprite = pygame.transform.scale(self.original_sprite, (self.sprite_widht, self.sprite_height))
        self.sprite = self.original_sprite
        self.rect = self.sprite.get_rect()
        self.offset_from_center = data["offset"]
        self.offset = pygame.Vector2(self.offset_from_center, 0)
        self.angle = 0

    def update(self, dt, camera=None):
        if isinstance(self.owner, Player):
            direction = self.owner.get_direction(camera)
        else:
            direction = self.owner.get_direction()
            
        self.angle = -math.degrees(math.atan2(direction.y, direction.x))
        sprite = self.original_sprite

        if direction.x >= 0:
            self.sprite = pygame.transform.rotate(sprite, self.angle)
        else:
            sprite = pygame.transform.flip(sprite, False, True)
            self.sprite = pygame.transform.rotate(sprite, self.angle)
        rotated_offset = self.offset.rotate(-self.angle)
        owner_center = pygame.Vector2(self.owner.rect.center)
        weapon_pos = (owner_center + rotated_offset)
        self.rect = self.sprite.get_rect(center=weapon_pos)
        

        if self.cooldown > 0:
            self.cooldown -= dt
    
    def can_shoot(self):
        return self.cooldown <= 0
    
    def render(self, screen, camera=None):
        rect = self.rect

        if camera is not None:
            rect = camera.apply(self.rect)

        screen.blit(self.sprite, rect)

class Melee(Weapon):
    def __init__(self, data: dict, combat_system: CombatSystem):
        super().__init__(data, combat_system)
        self.range = data["range"]

    def shoot(self):
        if self.can_shoot():
            if isinstance(self.owner, Player):
                self.combat_system.process_melee_attack(self.range, self.damage)
                self.cooldown = self.attack_rate
            elif isinstance(self.owner, Zombie):
                self.combat_system.process_zombie_melee_attack(self.damage)
                self.cooldown = self.attack_rate
    
class Ranged(Weapon):
    def __init__(self, data: dict, combat_system: CombatSystem):
        
        super().__init__(data, combat_system)
        self.mag_size = data["mag_size"]
        self.current_ammo = data["mag_size"]
        self.reload_time = data["reload_time"]
        self.bullet_speed = data["bullet_speed"]
        self.spread = data["spread"]
        self.pellets = data["pellets"]
        self.fire_mode = data["firemode"]
        self.reloading = False
        self.reload_timer = 0
    
    def update_ranged(self, dt, camera=None):
        super().update(dt, camera)
        
        if self.reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.finish_reload()
    
    def can_shoot(self):
        if self.cooldown <= 0 and self.current_ammo > 0:
            return True
        else:
            return False

    def shoot(self):
        if self.can_shoot() and self.current_ammo > 0 and not self.reloading:
            for _ in range(self.pellets):
                self.combat_system.spawn_bullet(self.damage, self.spread, self.bullet_speed)
            self.current_ammo -= 1
            self.cooldown = self.attack_rate
    
    def start_reload(self, input_state):
        if self.current_ammo < self.mag_size and not self.reloading and input_state.reloading_weapon:
            
            self.reloading = True
            self.reload_timer = self.reload_time

    def finish_reload(self):        
        need = self.mag_size - self.current_ammo
        take = min(need, self.owner.ammo)
        self.current_ammo += take
        self.owner.ammo -= take
        self.reloading = False
