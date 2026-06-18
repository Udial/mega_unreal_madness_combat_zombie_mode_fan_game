import os
import pygame
from ... import settings
from .player import Player
from ..systems.input_system import InputState
from ..systems.collision_system import CollisionSystem
from ..core.camera import Camera


class ComputerTerminal:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        sprite_path: str | None = None
    ):
        self.rect = pygame.Rect(x, y , width, height)

        self.interaction_rect = pygame.Rect(
            x - 40,
            y + width + 100,
            width + 80,
            80
        )
        self.can_interact = False

        self.sprite_path = sprite_path
        self.sprite = None

        if self.sprite_path is not None and os.path.exists(self.sprite_path):
            self.sprite = pygame.image.load(self.sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))
        
        self.last_interact = False

    def update(
        self,
        player: Player,
        collision_system: CollisionSystem,
        input_state: InputState
    ) -> bool:
        self.can_interact = self.can_player_interact(player, collision_system)

        interact_pressed_once = input_state.interact and not self.last_interact
        self.last_interact = input_state.interact

        return self.can_interact and interact_pressed_once
    
    def can_player_interact(
            self,
            player: Player,
            collsion_system: CollisionSystem
    ) -> bool:
        player_feet = collsion_system.get_player_feet_points(player.rect)

        if self.interaction_rect.collidepoint(player_feet[0]):
            return True
        
        if self.interaction_rect.collidepoint(player_feet[2]):
            return True
        
        return False
    
    def render(
        self,
        screen,
        camera: Camera = None
    ):
        rect = self.rect
        interaction_rect = self.interaction_rect

        if camera is not None:
            rect = camera.apply(self.rect)
            interaction_rect = camera.apply(self.interaction_rect)
        
        if self.sprite is not None:
            screen.blit(self.sprite, rect)
        else:
            pygame.draw.rect(screen, (30, 30, 30), rect)
            pygame.draw.rect(screen, settings.GREEN, rect, 3)
        
    def render_hint(self, screen, camera: Camera):
        if not self.can_interact:
            return
        
        font = pygame.font.SysFont(None, 28)
        text_surface = font.render("Press E to open shop", True, settings.WHITE)
        screen_x = self.rect.centerx 
        screen_y = self.rect.centery

        screen.blit(text_surface, text_surface.get_rect(center=(screen_x, screen_y)))