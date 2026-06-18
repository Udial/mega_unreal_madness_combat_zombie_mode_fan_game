from ...settings import HITBOX_HEIGHT, HITBOX_WIDTH
from ..entities.zombie import Zombie
from .weapon_factory import WeaponFactory
from ..entities.entry_point import EntryPoint
import random


class SpawnManager:
    def __init__(self, entry_points: list[EntryPoint], entities: list, weapon_factory: WeaponFactory):
        self.entry_points = entry_points
        self.entities = entities
        self.weapon_factory = weapon_factory

    def spawn_zombie(self, type: str, entry_index= None):
        if entry_index == None:
            entry = random.choice(self.entry_points)
        else:
            entry = self.entry_points[entry_index]
        
        spawn_x, spawn_y = entry.spawn_point
        x = spawn_x - HITBOX_WIDTH // 2
        y = spawn_y - HITBOX_HEIGHT // 2
        if entry.is_open():
            if type == "normal":
                weapon = self.weapon_factory.create_weapon("zombie_fists")
                zombie = Zombie(x, y)
                self.weapon_factory.assign_weapon(weapon, zombie)
            self.entities.append(zombie)
            
        elif not entry.is_open():
            entry.rapid_spawn_queue.append(type)