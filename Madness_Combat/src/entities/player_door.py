import pygame
from ... import settings
from ..systems.input_system import InputState
from .player import Player
from ..systems.collision_system import CollisionSystem
from ..core.camera import Camera


class PlayerDoor:
    def __init__(
        self,
        cords_tuple: tuple,
        target_room: str,
        target_pos: tuple,
        wall_pos: str
    ):
        self.target_room = target_room
        self.target_pos = target_pos

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

        self.rect = pygame.Rect(
            min(xs),
            min(ys),
            self.width,
            self.height
        )

        interaction_height = 60

        self.player_interaction_rect = pygame.Rect(
            min(xs),
            self.points[2][1],
            self.width if wall_pos == "top" else (self.width + 40 if wall_pos == "left" else self.width - 40),
            interaction_height
        )

    def update(
            self,
            player: Player,
            collision_system: CollisionSystem,
            input_state: InputState
        ) -> bool:

        if self.can_player_interact(player, collision_system) and input_state.interact:
            self.teleport_player(player)
            return True
        return False
    
    def can_player_interact(
            self,
            player: Player,
            collision_system: CollisionSystem,
    ) -> bool:
        player_feet = collision_system.get_player_feet_points(player.rect)
        collided = False

        if self.player_interaction_rect.collidepoint(player_feet[0]):
            collided = True
        elif self.player_interaction_rect.collidepoint(player_feet[2]):
            collided = True
        
        return collided
    
    def teleport_player(
            self,
            player: Player
    ):
        player.pos_x, player.pos_y = self.target_pos
        player.update_rect()

    def render(
            self,
            screen,
            camera: Camera=None
    ):
        points = self.points
        if camera is not None:
            points = camera.apply_points(self.points)
        pygame.draw.polygon(
            screen,
            (140, 140, 140),
            points,
            0
        )
        pygame.draw.polygon(
            screen,
            settings.BLACK,
            points,
            2
        )