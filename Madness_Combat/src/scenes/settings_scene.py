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
        
        self.resolution_1920x1080 = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID - 2*(settings.BASE_BUTTON_HEIGHT / 2)),
                            "1920x1080",
                            True,
                            )
        
        self.resolution_3440x1440 = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID - 5*(settings.BASE_BUTTON_HEIGHT / 2)),
                            "3440x1440",
                            True,
                            )


    def update(self, dt):
        pass

    def handle_event(self, event):
        return_to_menu = self.exit_button.is_clicked()

        resolution_1920x1080 = self.resolution_1920x1080.is_clicked()
        resolution_3440x1440 = self.resolution_3440x1440.is_clicked()

        if resolution_1920x1080:
            from ..core.game import Game
            self.game.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        if resolution_3440x1440:
            from ..core.game import Game
            settings.SCREEN_HEIGHT = 1440
            settings.SCREEN_WIDTH = 3440

            pygame.display.set_mode((3440, 1440))

            print(settings.SCREEN_HEIGHT)
            print(settings.SCREEN_HEIGHT_MID)
            

        if return_to_menu:
            from .main_menu_scene import MainMenuScene
            self.game.scene_manager.set_scene(MainMenuScene(self.game))


    def render(self, screen):
        screen.fill(settings.LIGHT_GRAY)

        title_surface = self.title_font.render("settings scene", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_surface, title_rect)

        self.exit_button.render(screen)
        self.resolution_1920x1080.render(screen)
        self.resolution_3440x1440.render(screen)
