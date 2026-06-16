import pygame 
from ..entities.player import Player
from ..entities.zombie import Zombie
from .combat_system import CombatSystem

class AISystem:
    def __init__(self, movement_system, player: Player):
        self.movement_system = movement_system
        self.player = player
    
    def update(self, zombies: list[Zombie], room_type: str, dt):
        for zombie in zombies:
            if zombie.get_distance_to(self.player) > zombie.weapon.range:
                input_state = self._build_input(zombie)
                self.movement_system.update(zombie, input_state, room_type, dt)
            else:
                zombie.weapon.shoot()

    def _build_input(self, zombie):
        direction = pygame.Vector2(
            self.player.pos_x - zombie.pos_x,
            self.player.pos_y - zombie.pos_y
        )
        
        if direction.length() > 0:
            direction = direction.normalize()

        class AIInput:
            def __init__(self, move):
                self.move = move
                self.shoot = False
        
        return AIInput(direction)