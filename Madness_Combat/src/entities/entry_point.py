import pygame
from .base_entity import BaseEntity
from .player import Player
from .barricade import Barricade
from ..systems.collision_system import CollisionSystem
from ..systems.input_system import InputState
from ...settings import BLACK


class EntryPoint(BaseEntity):
    def __init__(self, cords_tuple: tuple, entry_type: str):
        self.x_topleft, self.y_topleft = cords_tuple[0]
        self.x_topright, self.y_topright = cords_tuple[1]
        self.x_downrigth, self.y_downright = cords_tuple[2]
        self.x_downleft, self.y_downleft = cords_tuple[3]
        self.width = self.x_topright - self.x_topleft
        self.height = self.y_downleft - self.y_topleft

        self.player_interaction_rect = pygame.Rect(self.x_downleft, self.y_downleft, self.width, 50)

        super().__init__(self.x_topleft, self.y_topleft, self.width, self.height)
        
        self.barricade_placement_timer = 0
        self.barricade_placement_time = 3
        self.type = entry_type
        self.is_blocked = False
        self.spawn_point = self.rect.center

    def update(self, player: Player, collision_system: CollisionSystem, input_state: InputState, dt, barricade_list: list):
        x = self.player_interaction(player, collision_system, input_state, dt)

        if x:
            barricade = Barricade(self)
            barricade_list.append(barricade)
            self.place_barricade(barricade)
    
    def can_player_interact(self, player: Player, collision_system: CollisionSystem) -> bool:
        
        player_feet = collision_system.get_player_feet_points(player.rect)

        collided = False

        if self.player_interaction_rect.collidepoint(player_feet[0]):
            collided = True
        elif self.player_interaction_rect.collidepoint(player_feet[2]):
            collided = True

        return collided
    
    def player_interaction(self, player: Player, collision_system: CollisionSystem, input_state: InputState, dt) -> bool:
        
        player_is_near = self.can_player_interact(player, collision_system)
        
        interacting = input_state.interact

        if player_is_near and interacting and not self.is_blocked:
            self.barricade_placement_timer += dt

            if self.barricade_placement_timer >= self.barricade_placement_time:
                self.barricade_placement_timer = 0
                return True
        else:
            self.barricade_placement_timer = 0
            return False
    
    def is_open(self):
        return not self.is_blocked
    
    def place_barricade(self, barricade):
        self.barricade = barricade
        self.is_blocked = True

    def remove_barricade(self):
        self.barricade = None
        self.is_blocked = False

    def get_spawn_point(self):
        return self.spawn_point
    
    def render(self, screen, color):
        pygame.draw.polygon(screen, color, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 0)
        pygame.draw.polygon(screen, BLACK, ((self.x_topleft, self.y_topleft),(self.x_topright, self.y_topright),(self.x_downrigth, self.y_downright),(self.x_downleft, self.y_downleft)), 2)