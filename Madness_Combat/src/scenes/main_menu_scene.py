import pygame
from ... import settings
from ..core.base_scene import BaseScene
from ..scenes.game_scene import GameScene


class MainMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font = pygame.font.SysFont(None, 36)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.scene_manager.set_scene(GameScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False
    
    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(settings.BG_MENU_COLOR)

        title_surface = self.title_font.render("Main menu", True, settings.WHITE)
        start_surface = self.text_font.render("Press ENTER to start", True, settings.LIGHT_GRAY)
        exit_surface = self.text_font.render('Press ESC to exit', True, settings.LIGHT_GRAY)

        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 220))
        start_rect = start_surface.get_rect(center=(screen.get_width() // 2, 340))
        exit_rect = exit_surface.get_rect(center=(screen.get_width() // 2, 390))

        screen.blit(title_surface, title_rect)
        screen.blit(start_surface, start_rect)
        screen.blit(exit_surface, exit_rect)