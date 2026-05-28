import pygame
from ..core.base_scene import BaseScene
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
        
        self.window_entry = EntryPoint(settings.ENTRY_POINTS_TUPLE[0], 'window', 0)
        #self.left_door_entry = EntryPoint(settings.ENTRY_POINTS_TUPLE[1], 'door')
        #self.right_door_entry = EntryPoint(settings.ENTRY_POINTS_TUPLE[2], 'door')

        self.left_wall = Wall(settings.WALL_CORDS_TUPLE[0], False)
        self.right_wall = Wall(settings.WALL_CORDS_TUPLE[1], False)
        self.back_wall = Wall(settings.WALL_CORDS_TUPLE[2], False)
        self.roof = Wall(settings.WALL_CORDS_TUPLE[3], False)

        self.walls = [self.left_wall, self.right_wall, self.back_wall, self.roof]
        self.player = Player(800, 900, 50, 100, 500, 100)
        self.zombie_list = []
        self.projectile_list = []
        self.entry_points = [self.window_entry]
        self.barricade_list = []
        

        self.economy_manager = EconomyManager()
        self.damage_system = DamageSystem()
        self.combat_system = CombatSystem(self.player, self.economy_manager, self.damage_system, self.zombie_list, self.projectile_list)
        self.weapon_factory = WeaponFactory(self.combat_system)
        self.shop_manager = ShopManager(self.economy_manager, self.player)
        self.collision_system = CollisionSystem()
        self.input_system = InputSystem()
        self.movement_system = MovementSystem(self.collision_system)
        self.spawn_manager = SpawnManager(self.entry_points, self.zombie_list, self.weapon_factory)
        self.wave_manager = WaveManager(self.spawn_manager, self.zombie_list, self.entry_points)
        self.ai_system = AISystem(self.movement_system, self.player)

        players_weapon = self.weapon_factory.create_weapon("pistol")
        self.weapon_factory.assign_weapon(players_weapon, self.player)
        

    def handle_event(self, event):
        clicked = self.exit_button.is_clicked()

        if clicked:
            from .main_menu_scene import MainMenuScene
            self.game.scene_manager.set_scene(MainMenuScene(self.game))


    def update(self, dt):

        print(f"DEBUG Player health: {self.player.hp}")

        self.wave_manager.update(dt)

        if self.player.weapon != None:
            self.player.weapon.update(dt)
       
        input_state = self.input_system.get_input()

        if isinstance(self.player.weapon, Melee):
            self.player.weapon.update(dt)
        
        elif isinstance(self.player.weapon, Ranged):
            self.player.weapon.update_ranged(dt)
        
        if isinstance(self.player.weapon, Ranged):
            self.player.weapon.start_reload(input_state)


        self.shop_manager.buy(input_state)

        self.combat_system.attack(input_state)

        self.movement_system.update(self.player, input_state, dt)

        if self.player.weapon != None:
            if self.player.weapon == Ranged:
                self.player.weapon.start_reload(input_state)

        for ep in self.entry_points:
            ep.update(self.player, self.collision_system, input_state, self.damage_system, dt)

        #self.combat_system.process_bullets(input_state)

        zombies = [e for e in self.zombie_list if isinstance(e, Zombie)]

        for zombie in zombies:
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
            wall.render(screen, settings.DARK_GRAY)

        for ep in self.entry_points:
            ep.render(screen, settings.SLIGHTLY_BRIGHTER_DARK_GRAY)
        
        for ep in self.entry_points:
            if ep.barricade != None:
                ep.barricade.render(screen)

        for entity in self.zombie_list:
            entity.render(screen)

        self.exit_button.render(screen)

        self.player.render(screen, settings.WHITE, self.player.rect)

        for proj in self.projectile_list:
            proj.render(screen)