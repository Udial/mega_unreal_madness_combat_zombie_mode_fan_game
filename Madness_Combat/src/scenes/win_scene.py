import pygame
from ..core.base_scene import BaseScene
from ..ui.button import Button
from ... import settings


class WinScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont(None, 92)
        self.text_font = pygame.font.SysFont(None, 36)
        x = settings.CAMERA_WIDTH_MID - settings.BASE_BUTTON_WIDTH // 2
        self.restart_button = Button(
            settings.BASE_BUTTON_WIDTH,
            settings.BASE_BUTTON_HEIGHT,
            x,
            540,
            "Play again",
        )
        self.menu_button = Button(
            settings.BASE_BUTTON_WIDTH, settings.BASE_BUTTON_HEIGHT, x, 610, "Main menu"
        )

    def handle_event(self, event):
        if self.restart_button.handle_event(event):
            from .game_scene import GameScene

            self.game.scene_manager.set_scene(GameScene(self.game))
        elif self.menu_button.handle_event(event):
            from .main_menu_scene import MainMenuScene

            self.game.scene_manager.set_scene(MainMenuScene(self.game))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from .game_scene import GameScene

                self.game.scene_manager.set_scene(GameScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                from .main_menu_scene import MainMenuScene

                self.game.scene_manager.set_scene(MainMenuScene(self.game))

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((12, 28, 18))
        title = self.title_font.render("ALL WAVES COMPLETED", True, settings.GREEN)
        title_rect = title.get_rect(center=(settings.CAMERA_WIDTH_MID, 320))
        screen.blit(title, title_rect)
        hint = self.text_font.render(
            "You survived the zombie mode.", True, settings.WHITE
        )
        hint_rect = hint.get_rect(center=(settings.CAMERA_WIDTH_MID, 420))
        screen.blit(hint, hint_rect)
        self.restart_button.render(screen)
        self.menu_button.render(screen)
