import json
import pygame
from .spawn_manager import SpawnManager


class WaveManager:
    def __init__(self, spawn_manager: SpawnManager, zombie: list):
        self.spawn_manager = spawn_manager
        self.zombie = zombie

        with open("Madness_Combat/data/waves.json", "r") as file:
            data = json.load(file)
        
        self.waves = data["waves"]

        self.curent_wave_index = 0
        self.spawn_queue = []
        self.spawn_timer = 0

        self.is_in_break = False
        self.break_timer = 0
        self.break_duration = 5

        self.curent_spawn_delay = 1

        self.start_wave()


    def start_wave(self):
        wave_data = self.waves[self.curent_wave_index]

        self.spawn_queue.clear()

        for zombie_group in wave_data["zombies"]:
            
            zombie_type = zombie_group["type"]
            count = zombie_group["count"]

            for _ in range(count):
                self.spawn_queue.append(zombie_type)

        self.curent_spawn_delay = wave_data["spawn_delay"]

        self.spawn_timer = 0

        print(f"DEBUG wave {self.curent_wave_index + 1} started")


    def update(self, dt):
        if self.is_in_break:
            
            self.break_timer += dt

            if self.break_timer >= self.break_duration:

                self.break_timer = 0
                self.is_in_break = False

                self.curent_wave_index += 1

                if self.curent_wave_index >= len(self.waves):
                    print("DEBUG All waves completed")
                    return
            
                self.start_wave()
            
            return
        
        self.spawn_timer += dt

        if self.spawn_timer >= self.curent_spawn_delay:

            self.spawn_timer = 0

            if self.spawn_queue:

                zombie_type = self.spawn_queue.pop(0)
                
                self.spawn_manager.spawn_zombie(zombie_type)
        
        if not self.spawn_queue and not self.zombie:
            self.is_in_break = True
            print("DEBUG Wave completed")