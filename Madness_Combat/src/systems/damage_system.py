import pygame
from ..entities.zombie import Zombie
from ..systems.economy_manager import EconomyManager



class DamageSystem:
    def __init__(self, economy_manager: EconomyManager):
        self.economy_manager = economy_manager
        
    def apply_damage(self, target, damage):
        if target.armor > 0:
            if target.armor - damage < 0:
                leftover_damage = damage - target.armor
                target.armor = 0
                target.hp -= leftover_damage
            else:
                target.armor -= damage
        else:
            target.hp -= damage

        if target.hp <= 0:
            self.kill_entity(target)
            if isinstance(target, Zombie) and self.economy_manager != None:
                self.economy_manager.credits += target.reward
                print(f"DEBUG Player got {target.reward} credits")
    
    def kill_entity(self, entity):
        entity.is_alive = False