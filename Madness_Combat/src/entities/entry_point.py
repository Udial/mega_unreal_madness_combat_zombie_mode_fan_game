import pygame
from .base_entity import BaseEntity
from .player import Player
from .barricade import Barricade
from ..systems.collision_system import CollisionSystem
from ..systems.input_system import InputState
from ..systems.damage_system import DamageSystem
from ...settings import BLACK, ZOMBIE_DAMAGE


class EntryPoint(BaseEntity):
    def __init__(self, cords_tuple: tuple, entry_type: str, entry_index: int):
        self.entry_index = entry_index

        self.points = [
            cords_tuple[0],
            cords_tuple[1],
            cords_tuple[2],
            cords_tuple[3]
        ]

        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]

        self.width = max(xs) - min(xs)
        self.height = max(ys) - min(ys)

        super().__init__(
            min(xs),
            min(ys),
            self.width,
            self.height
        )
        interaction_height = 60

        self.player_interaction_rect = pygame.Rect(
            min(xs),
            max(ys) - interaction_height,
            self.width,
            interaction_height
        )

        self.barricade = None
        self.barricade_placement_timer = 0
        self.barricade_placement_time = 3
        self.type = entry_type
        self.is_blocked = False

        self.spawn_point = self.calculate_spawn_point()

        self.rapid_spawn_queue = []
        self.attack_timer = 0
        self.attack_time = 2

    def calculate_spawn_point(self):
        top_left, top_right, bottom_right, bottom_left = self.points

        bottom_center_x = (bottom_left[0] + bottom_right[0]) / 2
        bottom_center_y = (bottom_left[1] + bottom_right[1]) / 2

        if self.type == "top":
            return bottom_center_x, bottom_center_y
        if self.type == "left":
            return bottom_center_x + 40, bottom_center_y
        if self.type == "right":
            return bottom_center_x - 40, bottom_center_y

    def update(self, player: Player, collision_system: CollisionSystem, input_state: InputState, damage_system: DamageSystem, dt):
        x = self.player_interaction(player, collision_system, input_state, dt)

        if x:
            barricade = Barricade(self)
            self.place_barricade(barricade)

        if self.rapid_spawn_queue and self.is_blocked and self.barricade != None:
            if self.barricade.hp <= 0:
                self.remove_barricade()

            
            self.attack_timer += dt

            if self.attack_timer >= self.attack_time:
                damage_mult = len(self.rapid_spawn_queue)
                damage_system.apply_damage(self.barricade, ZOMBIE_DAMAGE * damage_mult)
                self.attack_timer = 0
                print("DEBUG Barricade damaged")


    
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

        if player_is_near and interacting and not self.is_blocked and player.amount_of_barricades >= 1:
            self.barricade_placement_timer += dt

            if self.barricade_placement_timer >= self.barricade_placement_time:
                self.barricade_placement_timer = 0
                player.amount_of_barricades -= 1
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
    
    def render(self, screen, color, camera=None):
        points = self.points
        
        if camera is not None:
            points = camera.apply_points(self.points)

        pygame.draw.polygon(screen, color, points, 0)
        pygame.draw.polygon(screen, BLACK, points, 2)