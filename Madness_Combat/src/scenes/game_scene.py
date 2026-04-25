import pygame
from ..core.base_scene import BaseScene
from ... import settings
from ..ui.button import Button
from ..entities.player import Player
from ..systems.input_system import InputSystem
from ..systems.movement_system import MovementSystem
from ..systems.collision_system import CollisionSystem
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
        
        self.player = Player(800, 900, 50, 100, 500, 100)

        self.input_system = InputSystem()
        self.collision_system = CollisionSystem()
        self.movement_system = MovementSystem(self.collision_system)

        self.left_wall = Wall(settings.WALL_CORDS_TUPLE[0], False)
        self.right_wall = Wall(settings.WALL_CORDS_TUPLE[1], False)
        self.back_wall = Wall(settings.WALL_CORDS_TUPLE[2], False)
        self.roof = Wall(settings.WALL_CORDS_TUPLE[3], False)
        

    def handle_event(self, event):
        clicked = self.exit_button.is_clicked()

        if clicked:
            from .main_menu_scene import MainMenuScene
            self.game.scene_manager.set_scene(MainMenuScene(self.game))


    def update(self, dt):
       
        input_state = self.input_system.get_input()

        self.movement_system.update(self.player, input_state, dt)


    def render(self, screen):
        screen.fill(settings.GRAY_COLOR_TEMP)

        title_surface = self.title_font.render("game scene", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_surface, title_rect)

        self.left_wall.render(screen, settings.DARK_GRAY)
        self.right_wall.render(screen, settings.DARK_GRAY)
        self.back_wall.render(screen, settings.DARK_GRAY)
        self.roof.render(screen, settings.DARK_GRAY)

        self.exit_button.render(screen)

        self.player.render(screen, settings.WHITE, self.player.rect)
