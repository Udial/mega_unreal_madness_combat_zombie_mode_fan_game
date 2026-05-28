import pygame
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

    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt
    
    def can_shoot(self):
        return self.cooldown <= 0

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
        self.reloading = False
        self.reload_timer = 0
    
    def update_ranged(self, dt):
        super().update(dt)
        
        if self.reloading:
            self.reload_timer -= dt
            print(f"DEBUG Reloading... Time left: {self.reload_timer}")
            if self.reload_timer <= 0:
                self.finish_reload()
                print("DEBUG Weapon Reloaded")
    
    def can_shoot(self):
        if self.cooldown <= 0 and self.current_ammo > 0:
            return True
        else:
            print("DEBUG Weapon can't shoot, no ammo or on cooldown")
            return False

    def shoot(self):
        if self.can_shoot() and self.current_ammo > 0 and not self.reloading:
            for _ in range(self.pellets):
                self.combat_system.spawn_bullet(self.damage)
            self.current_ammo -= 1
            self.cooldown = self.attack_rate
    
    def start_reload(self, input_state):
        if self.current_ammo < self.mag_size and not self.reloading and input_state.reloading_weapon:
            
            self.reloading = True
            self.reload_timer = self.reload_time
            print("DEBUG Started reloading")

    def finish_reload(self):        
        leftover_ammo = self.current_ammo
        self.owner.ammo += leftover_ammo
        self.owner.ammo -= self.mag_size
        self.current_ammo = self.mag_size
        self.reloading = False
