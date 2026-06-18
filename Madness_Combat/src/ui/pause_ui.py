import pygame


class PauseMenu:
    def __init__(self):
        self.is_open = False

        self.font = pygame.font.SysFont(None, 42)
        self.title_font = pygame.font.SysFont(None, 72)

        self.resume_button_rect = pygame.Rect(0, 0, 260, 60)
        self.exit_button_rect = pygame.Rect(0, 0, 260, 60)
        self.save_button_rect = pygame.Rect(0, 0, 260, 60)
        self.save_wipe_button_rect = pygame.Rect(0, 0, 260, 60)

    def toggle(self):
        self.is_open = not self.is_open

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def update_layout(self, screen):
        screen_rect = screen.get_rect()

        self.resume_button_rect.center = (
            screen_rect.centerx,
            screen_rect.centery - 100
        )
        
        self.save_button_rect.center = (
            screen_rect.centerx,
            screen_rect.centery - 20
        )

        self.save_wipe_button_rect.center = (
            screen_rect.centerx,
            screen_rect.centery + 60
        )

        self.exit_button_rect.center = (
            screen_rect.centerx,
            screen_rect.centery + 140
        )

    def handle_event(self, event):
        if not self.is_open:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            if self.resume_button_rect.collidepoint(mouse_pos):
                return "resume"

            if self.save_button_rect.collidepoint(mouse_pos):
                return "save"
            
            if self.save_wipe_button_rect.collidepoint(mouse_pos):
                return "wipe_save"

            if self.exit_button_rect.collidepoint(mouse_pos):
                return "exit"
            

        return None

    def render_button(self, screen, rect, text):
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            color = (90, 90, 90)
        else:
            color = (50, 50, 50)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (220, 220, 220), rect, 2)

        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)

    def render(self, screen):
        if not self.is_open:
            return

        self.update_layout(screen)

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        screen_rect = screen.get_rect()

        title_surface = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surface.get_rect(
            center=(screen_rect.centerx, screen_rect.centery - 180)
        )

        screen.blit(title_surface, title_rect)

        self.render_button(screen, self.resume_button_rect, "Resume")
        self.render_button(screen, self.save_button_rect, "Save")
        self.render_button(screen, self.save_wipe_button_rect, "Wipe save")
        self.render_button(screen, self.exit_button_rect, "Exit")