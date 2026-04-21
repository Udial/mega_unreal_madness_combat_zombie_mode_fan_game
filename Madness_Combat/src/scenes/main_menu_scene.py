import pygame
from ... import settings
from ..core.base_scene import BaseScene
from ..scenes.game_scene import GameScene
from ..ui.button import Button


class MainMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font = pygame.font.SysFont(None, 36)
        self.to_the_game_button = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID - (settings.BASE_BUTTON_HEIGHT / 2)),
                            "Play",
                            True,
                            )
        self.settings_button = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID + (2 * (settings.BASE_BUTTON_HEIGHT / 2))),
                            "Settings",
                            True,
                            )
        self.exit_button = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID + 2 * (2 * (settings.BASE_BUTTON_HEIGHT / 2))),
                            "Exit",
                            True,
                            )

    def handle_event(self, event):

        play = self.to_the_game_button.is_clicked()
        settings_tab = self.settings_button.is_clicked()
        exit = self.exit_button.is_clicked()


        if play:
            self.game.scene_manager.set_scene(GameScene(self.game))
        
        if exit:
            self.game.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.scene_manager.set_scene(GameScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False
    
    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(settings.BG_MENU_COLOR)

        self.to_the_game_button.render(screen)
        self.exit_button.render(screen)
        self.settings_button.render(screen)

        title_surface = self.title_font.render("Main menu", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 220))
        screen.blit(title_surface, title_rect)