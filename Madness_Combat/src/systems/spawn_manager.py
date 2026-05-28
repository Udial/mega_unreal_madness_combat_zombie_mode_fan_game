import pygame
from ...settings import ZOMBIE_SPAWN_TIMER, ZOMBIE_SPAWN_DELAY, ZOMBIE_RAPID_SPAWN_DELAY, ZOMBIE_RAPID_SPAWN_TIMER
from ..entities.zombie import Zombie
from .weapon_factory import WeaponFactory
import random


class SpawnManager:
    def __init__(self, entry_points: list, entities: list, weapon_factory: WeaponFactory):
        self.entry_points = entry_points
        self.entities = entities
        self.weapon_factory = weapon_factory

    def spawn_zombie(self, type: str, entry_index= None):
        if entry_index == None:
            entry = random.choice(self.entry_points)
        else:
            entry = self.entry_points[entry_index]
        
        x, y = entry.get_spawn_point()
        if entry.is_open():
            if type == "normal":
                weapon = self.weapon_factory.create_weapon("zombie_fists")
                zombie = Zombie(x, y)
                self.weapon_factory.assign_weapon(weapon, zombie)
            self.entities.append(zombie)
            print("DEBUG Zombie spawned")
            
        elif not entry.is_open():
            entry.rapid_spawn_queue.append(type)
            print("DEBUG Added zombie to rapid queue")