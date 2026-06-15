import pygame
from ..entities.player import Player
from ..systems.economy_manager import EconomyManager
from ..systems.wave_manager import WaveManager


class HUD:
    def __init__(self, player: Player, economy_manager: EconomyManager, wave_manager: WaveManager):
        self.player = player
        self.economy_manager = economy_manager
        self.wave_manager = wave_manager

        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)

        self.padding = 20
        self.line_height = 32

    def render_text(self, screen, text, x, y, color=(255, 255, 255)):
        surface = self.font.render(text, True, color)
        screen.blit(surface, (x, y))

    def render(self, screen):
        x = self.padding
        y = self.padding

        self.render_text(screen, f"HP: {self.player.hp}", x, y)
        y += self.line_height

        self.render_text(screen, f"Credits: {self.economy_manager.credits}", x, y)
        y += self.line_height

        self.render_text(screen, f"Barricades: {self.player.amount_of_barricades}", x, y)
        y += self.line_height

        self.render_weapon_info(screen, x, y)
        y += self.line_height

        self.render_wave_info(screen, x, y)

    def render_weapon_info(self, screen, x, y):
        weapon = self.player.weapon

        if weapon is None:
            self.render_text(screen, "Weapon: None", x, y)
            return

        weapon_name = weapon.name

        if hasattr(weapon, "current_ammo") and hasattr(weapon, "mag_size"):
            text = f"{weapon_name}: {weapon.current_ammo}/{weapon.mag_size} | Ammo: {self.player.ammo}"
        else:
            text = f"Weapon: {weapon_name}"

        self.render_text(screen, text, x, y)

    def render_wave_info(self, screen, x, y):
        wave_number = self.wave_manager.curent_wave_index + 1
        total_waves = len(self.wave_manager.waves)

        if self.wave_manager.is_in_break:
            text = f"Wave: {wave_number}/{total_waves} | Hold TAB to start"
            self.render_text(screen, text, x, y)
            self.render_wave_bar(screen, x , y + 36)
        else:
            zombies_left_to_spawn = len(self.wave_manager.spawn_queue)
            zombies_alive = len(self.wave_manager.zombie)
            text = f"Wave: {wave_number}/{total_waves} | Zombies: {zombies_alive} | Queue: {zombies_left_to_spawn}"

        self.render_text(screen, text, x, y)
    
    def render_wave_bar(self, screen, x, y):
        progress = self.wave_manager.get_start_wave_progress()

        bar_width = 160
        bar_height = 32

        border_color = (255, 255, 255)
        fill_color = (80, 220, 120)
        bg_color = (40, 40, 40)

        bar_rect = pygame.Rect(x, y, bar_width, bar_height)
        inner_rect = bar_rect.inflate(-6, -6)

        pygame.draw.rect(screen, bg_color, bar_rect)
        pygame.draw.rect(screen, border_color, bar_rect, 3)

        fill_width = int(inner_rect.width * progress)

        fill_rect = pygame.Rect(
            inner_rect.x,
            inner_rect.y,
            fill_width,
            inner_rect.height
        )

        pygame.draw.rect(screen, fill_color, fill_rect)