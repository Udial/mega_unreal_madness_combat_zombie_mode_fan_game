import pygame
import sys
from ... import settings
from ..scenes.main_menu_scene import MainMenuScene
from .scene_manager import SceneManager



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_NAME)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager()
        self.scene_manager.set_scene(MainMenuScene(self))
    
    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene_manager.handle_event(event)
            
            self.scene_manager.update(dt)
            self.scene_manager.render(self.screen)
        
            pygame.display.flip()