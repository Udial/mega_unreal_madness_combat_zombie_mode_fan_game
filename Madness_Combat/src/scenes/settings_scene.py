import pygame
from ..core.base_scene import BaseScene
from ..ui.button import Button
from ... import settings


class SettingsScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font = pygame.font.SysFont(None, 32)
        x = settings.CAMERA_WIDTH_MID - settings.BASE_BUTTON_WIDTH // 2
        self.resolution_1920x1080 = Button(
            settings.BASE_BUTTON_WIDTH, settings.BASE_BUTTON_HEIGHT, x, 430, "1920x1080"
        )
        self.resolution_3440x1440 = Button(
            settings.BASE_BUTTON_WIDTH, settings.BASE_BUTTON_HEIGHT, x, 500, "3440x1440"
        )
        self.exit_button = Button(
            settings.BASE_BUTTON_WIDTH, settings.BASE_BUTTON_HEIGHT, x, 610, "Back"
        )

    def update(self, dt):
        pass

    def _set_resolution(self, width, height):
        settings.SCREEN_WIDTH = width
        settings.SCREEN_HEIGHT = height
        settings.SCREEN_WIDTH_MID = width // 2
        settings.SCREEN_HEIGHT_MID = height // 2
        settings.CAMERA_SCREEN_WIDTH = width
        settings.CAMERA_SCREEN_HEIGHT = height
        self.game.screen = pygame.display.set_mode((width, height))

    def handle_event(self, event):
        if self.resolution_1920x1080.handle_event(event):
            self._set_resolution(1920, 1080)
        elif self.resolution_3440x1440.handle_event(event):
            self._set_resolution(3440, 1440)
        elif self.exit_button.handle_event(event) or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            from .main_menu_scene import MainMenuScene

            self.game.scene_manager.set_scene(MainMenuScene(self.game))

    def render(self, screen):
        screen.fill(settings.BG_MENU_COLOR)
        title_surface = self.title_font.render("Settings", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(title_surface, title_rect)
        info = self.text_font.render("Resolution", True, settings.LIGHT_GRAY)
        info_rect = info.get_rect(center=(screen.get_width() // 2, 370))
        screen.blit(info, info_rect)
        self.resolution_1920x1080.render(screen)
        self.resolution_3440x1440.render(screen)
        self.exit_button.render(screen)
