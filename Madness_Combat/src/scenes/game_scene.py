import pygame
from ..core.base_scene import BaseScene
from ... import settings
from ..ui.button import Button
from ..entities.player import Player
from ..systems.input_system import InputSystem
from ..systems.movement_system import MovementSystem
from ..entities.wall import Wall


class GameScene(BaseScene):
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
        
        self.player = Player(800, 1000, 50, 100, 500, 100)
        self.input_system = InputSystem()
        self.movement_system = MovementSystem()
        self.left_wall = Wall(0,0,200,100,200,980,0,1080,False)
        
        

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
        self.player.prev_pos_x = self.player.pos_x
        self.player.prev_pos_y = self.player.pos_y

        input_state = self.input_system.get_input()

        self.movement_system.update(self.player, input_state, dt)

        if self.player.check_if_point_is_beyond_wall(self.left_wall.collision_line, self.player.rect):
            self.player.pos_x = self.player.prev_pos_x

        if self.player.check_if_point_is_beyond_wall(self.left_wall.collision_line, self.player.rect):
            self.player.pos_y = self.player.prev_pos_y

    def render(self, screen):
        screen.fill(settings.GRAY_COLOR_TEMP)

        title_surface = self.title_font.render("game scene", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_surface, title_rect)

        self.exit_button.render(screen)
        self.left_wall.render(screen, settings.DARK_GRAY)

        self.player.render(screen, settings.WHITE, self.player.rect)
