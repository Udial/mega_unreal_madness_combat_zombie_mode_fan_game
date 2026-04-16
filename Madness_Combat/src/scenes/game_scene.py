import pygame
from ..core.base_scene import BaseScene
from ... import settings
from ..ui.button import Button


class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font = pygame.font.SysFont(None, 36)
        self.exit_button = mega_button = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID - (settings.BASE_BUTTON_HEIGHT / 2)),
                            "test_button",
                            True,
                            )
        

    def handle_event(self, event):
        clicked = self.exit_button.is_clicked()

        if clicked:
            from .main_menu_scene import MainMenuScene
            self.game.scene_manager.set_scene(MainMenuScene(self.game))
            
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from .main_menu_scene import MainMenuScene
                self.game.scene_manager.set_scene(MainMenuScene(self.game))

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(settings.GRAY_COLOR_TEMP)
        
        title_surface = self.title_font.render("game scene", True, settings.WHITE)
        hint_surface = self.text_font.render("press ESC to return to menu", True, settings.LIGHT_GRAY)

        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 200))
        hint_rect = hint_surface.get_rect(center=(screen.get_width() // 2, 340))

        screen.blit(title_surface, title_rect)
        screen.blit(hint_surface, hint_rect)

        self.exit_button.render(screen)
