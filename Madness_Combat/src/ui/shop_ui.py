import os
import pygame

from ... import settings
from ..systems.shop_manager import ShopManager


class ShopUI:
    def __init__(self, shop_manager: ShopManager):
        self.shop_manager = shop_manager
        self.is_open = False

        self.categories = [
            ("weapons", "Weapons"),
            ("ammo", "Ammo"),
            ("consumables", "Consumables"),
            ("armor", "Armor")
        ]

        self.selected_category = "weapons"

        self.title_font = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 34)
        self.small_font = pygame.font.SysFont(None, 26)

        self.sprite_cache = {}

        self.window_rect = pygame.Rect(160, 100, 1600, 820)
        self.category_rects = {}
        self.item_rects = []

        self.close_button_rect = pygame.Rect(
            self.window_rect.right - 54,
            self.window_rect.y + 18,
            36,
            36
        )
    
    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def handle_event(self, event):
        if not self.is_open:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_left_click(event.pos)
        
    def handle_left_click(self, mouse_pos: tuple):
        if self.close_button_rect.collidepoint(mouse_pos):
            self.close()
            return

        for category_id, rect in self.category_rects.items():
            if rect.collidepoint(mouse_pos):
                self.selected_category = category_id
            
        for item, rect in self.item_rects:
            if rect.collidepoint(mouse_pos):
                self.shop_manager.buy_item(self.selected_category, item)
                return
            
    def load_sprite(self, sprite_path: str | None, size: tuple):
        if sprite_path is None:
            return None
        
        if not os.path.exists(sprite_path):
            return None
        
        cache_key = (sprite_path, size)

        if cache_key not in self.sprite_cache:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, size)
            self.sprite_cache[cache_key] = sprite

        return self.sprite_cache[cache_key]
    
    def render(self, screen):
        if not self.is_open:
            return
        
        self.render_background(screen)
        self.render_window(screen)
        self.render_categories(screen)
        self.render_items(screen)
        self.render_message(screen)
        self.render_close_button(screen)

    def render_background(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

    def render_window(self, screen):
        pygame.draw.rect(screen, (20, 20, 20), self.window_rect)
        pygame.draw.rect(screen, settings.WHITE, self.window_rect, 3)

        title_surface = self.title_font.render("SHOP TERMINAL", True, settings.WHITE)
        screen.blit(title_surface, (self.window_rect.x + 24, self.window_rect.y + 20))

        credits_surface = self.font.render(
            f"Credits: {self.shop_manager.economy_manager.credits}",
            True,
            settings.WHITE
        )
        screen.blit(credits_surface, (self.window_rect.x + 24, self.window_rect.y + 70))

    def render_categories(self, screen):
        self.category_rects.clear()
        left_width = self.window_rect.width // 5
        category_area = pygame.Rect(
            self.window_rect.x,
            self.window_rect.y + 120,
            left_width,
            self.window_rect.height - 120
        )
        pygame.draw.rect(screen, (28, 28, 28), category_area)
        pygame.draw.line(
            screen,
            settings.WHITE,
            (category_area.right, category_area.y),
            (category_area.right, category_area.bottom),
            2
        )
        button_height = 70
        button_margin = 16
        y = category_area.y + button_margin
        for category_id, category_name in self.categories:
            rect = pygame.Rect(
                category_area.x + button_margin,
                y,
                category_area.width - button_margin * 2,
                button_height
            )
            self.category_rects[category_id] = rect
            if category_id == self.selected_category:
                color = (70, 70, 70)
            else:
                color = (42, 42, 42)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, settings.WHITE, rect, 2)
            text_surface = self.font.render(category_name, True, settings.WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
            y += button_height + button_margin

    def render_items(self, screen):
        self.item_rects.clear()
        left_width = self.window_rect.width // 5
        item_area = pygame.Rect(
            self.window_rect.x + left_width,
            self.window_rect.y + 120,
            self.window_rect.width - left_width,
            self.window_rect.height - 120
        )
        items = self.shop_manager.get_items_by_category(self.selected_category)
        card_margin = 18
        card_height = 130
        x = item_area.x + card_margin
        y = item_area.y + card_margin
        for item in items:
            card_rect = pygame.Rect(
                x,
                y,
                item_area.width - card_margin * 2,
                card_height
            )
            self.item_rects.append((item, card_rect))
            pygame.draw.rect(screen, (35, 35, 35), card_rect)
            pygame.draw.rect(screen, settings.WHITE, card_rect, 2)
            icon_rect = pygame.Rect(

                card_rect.x + 18,
                card_rect.y + 20,
                110,
                70
            )
            sprite = self.load_sprite(item.get("sprite"), (icon_rect.width, icon_rect.height))

            if sprite is not None:
                screen.blit(sprite, icon_rect)
            else:
                # Временный fallback для предметов без спрайта.
                # Когда добавишь sprite path в json, он перестанет использоваться.
                pygame.draw.rect(screen, (60, 60, 60), icon_rect)
                pygame.draw.rect(screen, settings.WHITE, icon_rect, 1)

            name_surface = self.font.render(item["name"], True, settings.WHITE)
            screen.blit(name_surface, (card_rect.x + 150, card_rect.y + 18))

            description_surface = self.small_font.render(
                item["description"],
                True,
                settings.LIGHT_GRAY
            )
            screen.blit(description_surface, (card_rect.x + 150, card_rect.y + 58))
            price_surface = self.font.render(
                f"${item['price']}",
                True,
                settings.GREEN
            )
            screen.blit(price_surface, (card_rect.right - 140, card_rect.y + 44))
            y += card_height + card_margin
        if len(items) == 0:
            text_surface = self.font.render("No items available", True, settings.LIGHT_GRAY)
            screen.blit(text_surface, (item_area.x + 30, item_area.y + 30))

    def render_message(self, screen):
        if self.shop_manager.last_message == "":
            return
        message_surface = self.small_font.render(
            self.shop_manager.last_message,
            True,
            settings.WHITE
        )
        screen.blit(
            message_surface,
            (
                self.window_rect.x + 24,
                self.window_rect.bottom - 40
            )
        )

    def render_close_button(self, screen):
        pygame.draw.rect(screen, (80, 30, 30), self.close_button_rect)
        pygame.draw.rect(screen, settings.WHITE, self.close_button_rect, 2)
        text_surface = self.font.render("X", True, settings.WHITE)
        text_rect = text_surface.get_rect(center=self.close_button_rect.center)
        screen.blit(text_surface, text_rect)