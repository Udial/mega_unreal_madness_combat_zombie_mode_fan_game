import json
from .input_system import InputState
from .spawn_manager import SpawnManager
from ..entities.entry_point import EntryPoint
from ...settings import ZOMBIE_RAPID_SPAWN_DELAY


class WaveManager:
    def __init__(
        self, spawn_manager: SpawnManager, zombie: list, entry_points: list[EntryPoint]
    ):
        self.spawn_manager = spawn_manager
        self.zombie = zombie
        self.entry_points = entry_points
        with open("Madness_Combat/data/waves.json", "r") as file:
            data = json.load(file)
        self.waves = data["waves"]
        self.current_wave_index = -1
        self.spawn_queue = []
        self.spawn_timer = 0
        self.rapid_spawn_timer = 0
        self.rapid_spawn_delay = ZOMBIE_RAPID_SPAWN_DELAY
        self.is_in_break = True
        self.all_waves_completed = False
        self.tab_hold_duration = 0
        self.wave_start_timer = 3
        self.current_spawn_delay = 1

    def start_wave(self):
        if self.current_wave_index >= len(self.waves):
            self.all_waves_completed = True
            self.is_in_break = False
            self.spawn_queue.clear()
            return
        wave_data = self.waves[self.current_wave_index]
        self.spawn_queue.clear()
        for zombie_group in wave_data["zombies"]:
            zombie_type = zombie_group["type"]
            count = zombie_group["count"]
            for _ in range(count):
                self.spawn_queue.append(zombie_type)
        self.current_spawn_delay = wave_data["spawn_delay"]
        self.spawn_timer = 0

    def update(self, dt, input_state: InputState):
        if self.all_waves_completed:
            return
        if self.is_in_break:
            if input_state.starting_wave:
                self.tab_hold_duration += dt
            else:
                self.tab_hold_duration = 0
            if self.tab_hold_duration >= self.wave_start_timer:
                self.tab_hold_duration = 0
                self.is_in_break = False
                self.current_wave_index += 1
                if self.current_wave_index >= len(self.waves):
                    self.all_waves_completed = True
                    self.is_in_break = False
                    self.spawn_queue.clear()
                    return
                self.start_wave()
            return

        self.spawn_timer += dt
        if self.spawn_timer >= self.current_spawn_delay:
            self.spawn_timer = 0
            if self.spawn_queue and self.spawn_manager.can_spawn():
                zombie_type = self.spawn_queue[0]
                if self.spawn_manager.spawn_zombie(zombie_type):
                    self.spawn_queue.pop(0)

        self.rapid_spawn_timer += dt
        if (
            self.rapid_spawn_timer >= self.rapid_spawn_delay
            and self.spawn_manager.can_spawn()
        ):
            self.rapid_spawn_timer = 0
            for ep in self.entry_points:
                if ep.rapid_spawn_queue and not ep.is_blocked:
                    zombie_type = ep.rapid_spawn_queue[0]
                    if self.spawn_manager.spawn_zombie(zombie_type, ep.entry_index):
                        ep.rapid_spawn_queue.pop(0)
                    break

        barricaded_queues_empty = all(
            not ep.rapid_spawn_queue for ep in self.entry_points
        )
        if not self.spawn_queue and not self.zombie and barricaded_queues_empty:
            is_last_wave = self.current_wave_index >= len(self.waves) - 1
            if is_last_wave:
                self.all_waves_completed = True
                self.is_in_break = False
                self.spawn_queue.clear()
                return
            self.is_in_break = True

    def get_start_wave_progress(self) -> int:
        if self.tab_hold_duration <= 0:
            return 0
        return min(1, self.tab_hold_duration / self.wave_start_timer)
