import pygame
from ..core.base_scene import BaseScene
from ..ui.button import Button
from ... import settings

class SettingsScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        
        self.title_font = pygame.font.SysFont(None, 72)

        self.exit_button = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID - (settings.BASE_BUTTON_HEIGHT / 2)),
                            "Exit",
                            True,
                            )


    def update(self, dt):
        pass

    def handle_event(self, event):
        return_to_menu = self.exit_button.is_clicked()

        if return_to_menu:
            from .main_menu_scene import MainMenuScene
            self.game.scene_manager.set_scene(MainMenuScene(self.game))


    def render(self, screen):
        screen.fill(settings.LIGHT_GRAY)

        title_surface = self.title_font.render("settings scene", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_surface, title_rect)

        self.exit_button.render(screen)
