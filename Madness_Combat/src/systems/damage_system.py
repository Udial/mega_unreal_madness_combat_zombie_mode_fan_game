import pygame
from ..entities.zombie import Zombie
from ..systems.economy_manager import EconomyManager



class DamageSystem:
    def apply_damage(self, target, damage, economy_manager: EconomyManager=None):
        target.hp -= damage

        if target.hp <= 0:
            self.kill_entity(target)
            if isinstance(target, Zombie):
                economy_manager.credits += target.reward
                print(f"DEBUG Player got {target.reward} credits")
            
    def zombie_damage_dealer(self, target, damage):
        target.hp -= damage
        
        if target.hp <= 0:
            self.kill_entity(target)
    
    def kill_entity(self, entity):
        entity.is_alive = False