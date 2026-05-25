import pygame
from ...settings import ZOMBIE_SPAWN_TIMER, ZOMBIE_SPAWN_DELAY, ZOMBIE_RAPID_SPAWN_DELAY, ZOMBIE_RAPID_SPAWN_TIMER
from ..entities.zombie import Zombie
import random


class SpawnManager:
    def __init__(self, entry_points: list, entities: list):
        self.entry_points = entry_points
        self.entities = entities

    def spawn_zombie(self, type: str, entry_index= None):
        if entry_index == None:
            entry = random.choice(self.entry_points)
        else:
            entry = self.entry_points[entry_index]
        
        x, y = entry.get_spawn_point()
        if entry.is_open():
            if type == "normal":
                zombie = Zombie(x, y)
            self.entities.append(zombie)
            print("DEBUG Zombie spawned")
            
        elif not entry.is_open():
            entry.rapid_spawn_queue.append(type)
            print("DEBUG Added zombie to rapid queue")