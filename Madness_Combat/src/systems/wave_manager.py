import json
from .input_system import InputState
from .spawn_manager import SpawnManager
from ..entities.entry_point import EntryPoint
from ...settings import ZOMBIE_RAPID_SPAWN_DELAY


class WaveManager:
    def __init__(self, spawn_manager: SpawnManager, zombie: list, entry_points: list[EntryPoint]):
        self.spawn_manager = spawn_manager
        self.zombie = zombie
        self.entry_points = entry_points

        with open("Madness_Combat/data/waves.json", "r") as file:
            data = json.load(file)
        
        self.waves = data["waves"]

        self.curent_wave_index = 0
        self.spawn_queue = []
        self.spawn_timer = 0
        self.rapid_spawn_timer = 0
        self.rapid_spawn_delay = ZOMBIE_RAPID_SPAWN_DELAY

        self.is_in_break = False
        self.tab_hold_duration = 0
        self.wave_start_timer = 3

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


    def update(self, dt, input_state: InputState):
        if self.is_in_break:
            
            if input_state.starting_wave: 
                self.tab_hold_duration += dt
            else:
                self.tab_hold_duration = 0

            if self.tab_hold_duration >= self.wave_start_timer:

                self.tab_hold_duration = 0
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

                print("DEBUG Attempted to spawn a zombie")

        for ep in self.entry_points:
            if ep.rapid_spawn_queue and not ep.is_blocked:
                if self.spawn_timer >= self.rapid_spawn_delay:
                    self.spawn_timer = 0

                    zombie = ep.rapid_spawn_queue.pop(0)
                    self.spawn_manager.spawn_zombie(zombie, ep.entry_index)
                    print("DEBUG Attempting to spawn queued zombie")
                    
                    
        barricaded_zombies_killed = False
        for ep in self.entry_points:
            if ep.rapid_spawn_queue:
                barricaded_zombies_killed = False
                return
            else:
                barricaded_zombies_killed = True

        if not self.spawn_queue and not self.zombie and barricaded_zombies_killed:
            self.is_in_break = True
            print("DEBUG Wave completed")

    def get_start_wave_progress(self) -> int:
        if self.tab_hold_duration <= 0:
            return 0
        return min(1, self.tab_hold_duration / self.wave_start_timer)