import pygame
from ..core.base_scene import BaseScene
from ..core.camera import Camera
from ... import settings
from ..ui.button import Button
from ..entities.player import Player
from ..entities.wall import Wall
from ..entities.entry_point import EntryPoint
from ..entities.zombie import Zombie
from ..entities.bullet import Bullet
from ..entities.weapon import Ranged, Melee
from ..systems.input_system import InputSystem
from ..systems.movement_system import MovementSystem
from ..systems.collision_system import CollisionSystem
from ..systems.spawn_manager import SpawnManager
from ..systems.wave_manager import WaveManager
from ..systems.ai_system import AISystem
from ..systems.combat_system import CombatSystem
from ..systems.damage_system import DamageSystem
from ..systems.economy_manager import EconomyManager
from ..systems.shop_manager import ShopManager
from ..systems.weapon_factory import WeaponFactory
from ..ui.hud import HUD

from ..utils.geometry import make_wall_entry

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        self.camera = Camera(
            settings.CAMERA_SCREEN_WIDTH,
            settings.SCREEN_WIDTH,
            settings.MAX_CAMERA_X
        )

        self.title_font = pygame.font.SysFont(None, 72)
        self.exit_button = Button(settings.BASE_BUTTON_WIDTH, 
                            settings.BASE_BUTTON_HEIGHT, 
                            (settings.SCREEN_WIDTH_MID - (settings.BASE_BUTTON_WIDTH / 2)),
                            (settings.SCREEN_HEIGHT_MID - (settings.BASE_BUTTON_HEIGHT / 2)),
                            "Exit",
                            True,
                            )
        
        self.window_entry = EntryPoint(
            settings.ENTRY_POINTS_TUPLE[0],
            'window',
            0
        )

        left_door_points = make_wall_entry(
            settings.WALL_CORDS_TUPLE[0],
            u1 = 0.4,
            u2 = 0.6,
            v_top = 0.8,
            v_bottom = 1
        )
        right_door_ponts = make_wall_entry(
            settings.WALL_CORDS_TUPLE[1],
            u1 = 0.4,
            u2 = 0.6,
            v_top = 0.8,
            v_bottom = 1
        )

        self.left_door_entry = EntryPoint(
            left_door_points, "door", 1
        )
        self.right_door_entry = EntryPoint(
            right_door_ponts, "door", 2
        )

        self.left_wall = Wall(settings.WALL_CORDS_TUPLE[0], False)
        self.right_wall = Wall(settings.WALL_CORDS_TUPLE[1], False)
        self.back_wall = Wall(settings.WALL_CORDS_TUPLE[2], False)
        self.roof = Wall(settings.WALL_CORDS_TUPLE[3], False)

        self.walls = [
            self.left_wall,
            self.right_wall,
            self.back_wall,
            self.roof
        ]
        self.player = Player(800, 900, 50, 100, 500, 100)
        self.zombie_list = []
        self.projectile_list = []
        self.entry_points = [
            self.window_entry,
            self.left_door_entry,
            self.right_door_entry
        ]
        self.barricade_list = []
        

        self.economy_manager = EconomyManager()
        self.damage_system = DamageSystem(
            self.economy_manager
        )
        self.combat_system = CombatSystem(
            self.player,
            self.economy_manager,
            self.damage_system,
            self.zombie_list,
            self.projectile_list,
            self.camera
        )
        self.weapon_factory = WeaponFactory(
            self.combat_system
        )
        self.shop_manager = ShopManager(
            self.economy_manager,
            self.player
        )
        self.collision_system = CollisionSystem()
        self.input_system = InputSystem()
        self.movement_system = MovementSystem(
            self.collision_system
        )
        self.spawn_manager = SpawnManager(
            self.entry_points,
            self.zombie_list,
            self.weapon_factory
        )
        self.wave_manager = WaveManager(
            self.spawn_manager,
            self.zombie_list,
            self.entry_points
        )
        self.ai_system = AISystem(
            self.movement_system,
            self.player
        )
        self.hud = HUD(
            self.player,
            self.economy_manager,
            self.wave_manager
        )

        players_weapon = self.weapon_factory.create_weapon("M16")
        self.weapon_factory.assign_weapon(players_weapon, self.player)
        

    def handle_event(self, event):
        clicked = self.exit_button.is_clicked()

        if clicked:
            from .main_menu_scene import MainMenuScene
            self.game.scene_manager.set_scene(MainMenuScene(self.game))


    def update(self, dt):

        self.wave_manager.update(dt)

        if isinstance(self.player.weapon, Melee):
            self.player.weapon.update(dt, self.camera)    
              
        if isinstance(self.player.weapon, Ranged):
            self.player.weapon.update_ranged(dt, self.camera)         
       
        input_state = self.input_system.get_input()

        if isinstance(self.player.weapon, Ranged):
            self.player.weapon.start_reload(
                input_state
            )      

        self.shop_manager.buy(
            input_state
        )

        self.combat_system.attack(
            input_state
        )

        self.movement_system.update(
            self.player,
            input_state,
            dt
        )

        self.camera.update(self.player)

        if self.player.weapon != None:
            if self.player.weapon == Ranged:
                self.player.weapon.start_reload(
                    input_state
                )

        for ep in self.entry_points:
            ep.update(
                self.player,
                self.collision_system,
                input_state, self.damage_system,
                dt
            )

        zombies = [e for e in self.zombie_list if isinstance(e, Zombie)]

        for zombie in zombies:
            zombie.update_direction(self.player)
            zombie.weapon.update(dt)
        
        projectiles = [e for e in self.projectile_list if isinstance(e, Bullet)]

        self.ai_system.update(zombies, dt)

        for proj in projectiles:
            proj.update(dt)

        self.combat_system.process_bullets()

        self.projectile_list[:] = [e for e in self.projectile_list if e.is_alive]
        self.zombie_list[:] = [e for e in self.zombie_list if e.is_alive]


    def render(self, screen):
        screen.fill(settings.GRAY_COLOR_TEMP)

        title_surface = self.title_font.render("game scene", True, settings.WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_surface, title_rect)

        
        for wall in self.walls:
            wall.render(screen, settings.DARK_GRAY, self.camera)

        for ep in self.entry_points:
            ep.render(screen, settings.SLIGHTLY_BRIGHTER_DARK_GRAY, self.camera)
        
        for ep in self.entry_points:
            if ep.barricade != None:
                ep.barricade.render(screen, self.camera)

        for zombie in self.zombie_list:
            zombie.render(screen, self.camera)
            zombie.weapon.render(screen, self.camera)

        self.exit_button.render(screen)

        self.player.render(screen, settings.WHITE, self.camera)
        self.player.weapon.render(screen, self.camera)

        for proj in self.projectile_list:
            proj.render(screen, self.camera)

        self.hud.render(screen)