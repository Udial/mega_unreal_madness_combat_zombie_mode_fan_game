import pygame
from ...settings import ZOMBIE_SPAWN_TIMER, ZOMBIE_SPAWN_DELAY
from ..entities.zombie import Zombie
import random


class SpawnManager:
    def __init__(self, entry_points: list, entities: list):
        self.entry_points = entry_points
        self.entities = entities

        self.spawn_timer = ZOMBIE_SPAWN_TIMER
        self.spawn_delay = ZOMBIE_SPAWN_DELAY

    def update(self, dt):
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_zombie()

    def spawn_zombie(self):
        avalible_entries = [
            ep for ep in self.entry_points if ep.is_open()
        ]

        if not avalible_entries:
            return
        
        entry = random.choice(avalible_entries)

        x, y = entry.get_spawn_point()
        
        zombie = Zombie(x, y)

        self.entities.append(zombie)