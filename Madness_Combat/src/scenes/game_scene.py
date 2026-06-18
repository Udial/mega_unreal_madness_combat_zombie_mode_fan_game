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
from ..entities.player_door import PlayerDoor
from ..entities.computer_terminal import ComputerTerminal
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
from ..systems.save_manager import SaveManager
from ..ui.hud import HUD
from ..ui.shop_ui import ShopUI
from ..ui.pause_ui import PauseMenu

from ..utils.geometry import make_wall_entry

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        self.current_room = "arena"


        self.camera = Camera(
            settings.CAMERA_SCREEN_WIDTH,
            settings.WORLD_WIDTH,
            settings.MAX_CAMERA_X_ARENA
        )

        self.shop_room_door = PlayerDoor(
            settings.ENTRY_POINTS_TUPLE[2],
            "shop_room",
            (120, 850),
            "top"
        )

        shop_exit_points = make_wall_entry(
            settings.WALL_CORDS_TUPLE_SHOP[0],
            u1 = 0.4,
            u2 = 0.6,
            v_top = 0.8,
            v_bottom = 1
        )
        
        self.shop_room_exit_door = PlayerDoor(
            shop_exit_points,
            "arena",
            self.shop_room_door.rect.center,
            "left"
        )

        self.window_entry_left = EntryPoint(
            settings.ENTRY_POINTS_TUPLE[0],
            'top',
            0
        )

        self.window_entry_right = EntryPoint(
            settings.ENTRY_POINTS_TUPLE[1],
            'top',
            1
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
            left_door_points,
            "left",
            2
        )
        self.right_door_entry = EntryPoint(
            right_door_ponts,
            "right",
            3
        )

        self.left_wall = Wall(settings.WALL_CORDS_TUPLE[0], False)
        self.right_wall = Wall(settings.WALL_CORDS_TUPLE[1], False)
        self.back_wall = Wall(settings.WALL_CORDS_TUPLE[2], False)
        self.roof = Wall(settings.WALL_CORDS_TUPLE[3], False)

        self.shop_left_wall = Wall(settings.WALL_CORDS_TUPLE_SHOP[0], False)
        self.shop_right_wall = Wall(settings.WALL_CORDS_TUPLE_SHOP[1], False)
        self.shop_back_wall = Wall(settings.WALL_CORDS_TUPLE_SHOP[2], False)
        self.shop_roof = Wall(settings.WALL_CORDS_TUPLE_SHOP[3], False)

        self.walls = [
            self.left_wall,
            self.right_wall,
            self.back_wall,
            self.roof
        ]

        self.shop_walls = [
            self.shop_left_wall,
            self.shop_right_wall,
            self.shop_back_wall,
            self.shop_roof
        ]

        self.shop_terminal = ComputerTerminal(
            820,
            430,
            280,
            220
        )

        self.player = Player(
            800,
            900,
            settings.HITBOX_WIDTH,
            settings.HITBOX_HEIGHT,
            500,
            40
        )

        self.zombie_list = []
        self.projectile_list = []
        self.entry_points = [
            self.window_entry_left,
            self.window_entry_right,
            self.left_door_entry,
            self.right_door_entry,
        ]
        self.barricade_list = []
        self.active_player_doors = []
        

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
            self.player,
            self.weapon_factory
        )
        self.collision_system = CollisionSystem(
            self.walls,
            self.shop_walls
        )
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
        self.save_manager = SaveManager()
        self.ai_system = AISystem(
            self.movement_system,
            self.player
        )
        self.hud = HUD(
            self.player,
            self.economy_manager,
            self.wave_manager
        )
        self.shop_ui = ShopUI(
            self.shop_manager
        )
        self.pause_menu = PauseMenu()
        

        players_weapon = self.weapon_factory.create_weapon("pistol")
        self.weapon_factory.assign_weapon(players_weapon, self.player)
        self.save_manager.load_game(self)
        

    def handle_event(self, event):
        if self.pause_menu.is_open:
            pause_action = self.pause_menu.handle_event(event)

            if pause_action == "resume":
                self.pause_menu.close()
            elif pause_action == "save":
                self.save_manager.save_game(self)
            elif pause_action == "wipe_save":
                self.save_manager.reset_save()
                from .game_scene import GameScene
                self.game.scene_manager.set_scene(GameScene(self.game))
            elif pause_action == "exit":
                self.save_manager.save_game(self)
                from .main_menu_scene import MainMenuScene
                self.game.scene_manager.set_scene(MainMenuScene(self.game))
            return
        
        self.shop_ui.handle_event(event)
        if self.shop_ui.is_open:
            return
        


    def update(self, dt):

        input_state = self.input_system.get_input()

        if input_state.pause_pressed:
            if self.shop_ui.is_open:
                self.shop_ui.close()
            else:
                self.pause_menu.toggle()
        
        if self.pause_menu.is_open:
            return

        if self.shop_ui.is_open:
            self.camera.update(self.player)
            return
        
        if self.current_room == "arena":
            self.active_player_doors = [self.shop_room_door]
            self.camera.max_x = settings.MAX_CAMERA_X_ARENA

            self.wave_manager.update(
            dt,
            input_state
        )
            
            self.combat_system.attack(
            input_state
        )
            
        elif self.current_room == "shop_room":
            self.active_player_doors = [self.shop_room_exit_door]
            self.camera.max_x = settings.MAX_CAMERA_X_SHOP

            if self.shop_terminal.update(
                self.player,
                self.collision_system,
                input_state
            ):
                self.shop_ui.open()

        for door in self.active_player_doors:
            if self.wave_manager.is_in_break and door.update(
                self.player,
                self.collision_system,
                input_state
            ):
                self.current_room = door.target_room
                self.camera.update(self.player)
                break

        if isinstance(self.player.weapon, Melee):
            self.player.weapon.update(dt, self.camera)    
              
        if isinstance(self.player.weapon, Ranged):
            self.player.weapon.update_ranged(dt, self.camera)         

        
        if isinstance(self.player.weapon, Ranged):
            self.player.weapon.start_reload(
                input_state
            )      

        self.movement_system.update(
            self.player,
            input_state,
            self.current_room,
            dt
        )

        self.camera.update(self.player)
        
        for ep in self.entry_points:
            ep.update(
                self.player,
                self.collision_system,
                input_state,
                self.damage_system,
                dt
            )

        zombies = [e for e in self.zombie_list if isinstance(e, Zombie)]

        for zombie in zombies:
            zombie.update_direction(self.player)
            zombie.weapon.update(dt)
        
        projectiles = [e for e in self.projectile_list if isinstance(e, Bullet)]

        self.ai_system.update(zombies, self.current_room, dt)

        for proj in projectiles:
            proj.update(dt)

        self.combat_system.process_bullets()

        self.projectile_list[:] = [e for e in self.projectile_list if e.is_alive]
        self.zombie_list[:] = [e for e in self.zombie_list if e.is_alive]


    def render(self, screen):
        screen.fill(settings.GRAY_COLOR_TEMP)

        if self.current_room == "arena":

            for wall in self.walls:
                wall.render(screen, settings.DARK_GRAY, self.camera)
            
            self.shop_room_door.render(
                screen,
                self.camera
            )

            for ep in self.entry_points:
                ep.render(screen, settings.SLIGHTLY_BRIGHTER_DARK_GRAY, self.camera)
        
            for ep in self.entry_points:
                if ep.barricade != None:
                    ep.barricade.render(screen, self.camera)
            
            for zombie in self.zombie_list:
                zombie.render(screen, self.camera)
                zombie.weapon.render(screen, self.camera)
            
            for proj in self.projectile_list:
                proj.render(screen, self.camera)
        
        elif self.current_room == "shop_room":
            for wall in self.shop_walls:
                wall.render(screen, settings.DARK_GRAY, self.camera)

            self.shop_room_exit_door.render(
                screen,
                self.camera
            )

            self.shop_terminal.render(
                screen,
                self.camera
            )
            self.shop_terminal.render_hint(
                screen,
                self.camera
            )

        self.player.render(screen, settings.WHITE, self.camera)
        self.player.weapon.render(screen, self.camera)

        self.hud.render(screen)
        self.shop_ui.render(screen)

        self.pause_menu.render(screen)