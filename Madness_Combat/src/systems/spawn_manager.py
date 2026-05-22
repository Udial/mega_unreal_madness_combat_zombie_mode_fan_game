import pygame
from ...settings import ZOMBIE_SPAWN_TIMER, ZOMBIE_SPAWN_DELAY, ZOMBIE_RAPID_SPAWN_DELAY, ZOMBIE_RAPID_SPAWN_TIMER
from ..entities.zombie import Zombie
import random


class SpawnManager:
    def __init__(self, entry_points: list, entities: list):
        self.entry_points = entry_points
        self.entities = entities
        self.spawn_timer = ZOMBIE_SPAWN_TIMER
        self.spawn_delay = ZOMBIE_SPAWN_DELAY
        self.rapid_spawn_timer = ZOMBIE_RAPID_SPAWN_TIMER
        self.rapid_spawn_delay = ZOMBIE_RAPID_SPAWN_DELAY

    def update(self, dt):
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_zombie()

    def spawn_zombie(self, type: str):
        entry = random.choice(self.entry_points)

        x, y = entry.get_spawn_point()
        if entry.is_open():
            if type == "normal":
                zombie = Zombie(x, y)
            self.entities.append(zombie)
        elif not entry.is_open():
            entry.rapid_spawn_queue.append(type)
        
        if self.entities:
            print("DEBUG Zombie spawned")

    def rapid_spawn(self, spawn_list: list, dt):
        n = len(spawn_list)
        i = 0

        while i <= n - 1:
            self.rapid_spawn_timer += dt

            if self.rapid_spawn_delay <= self.rapid_spawn_timer:
                zombie = spawn_list.pop(0)
                self.spawn_zombie(zombie)
                i += 1
                print("DEBUG RAPID QUEUE ZOMBIE SPAWNED")
