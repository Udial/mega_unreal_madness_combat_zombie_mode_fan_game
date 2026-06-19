import pygame
from ... import settings


class Button:
    def __init__(
        self,
        width: int,
        height: int,
        x_pos: int,
        y_pos: int,
        text: str,
        enabled: bool = True,
        screen=None,
        font=None,
    ):
        self.width = int(width)
        self.height = int(height)
        self.x_pos = int(x_pos)
        self.y_pos = int(y_pos)
        self.enabled = enabled
        self.text = text
        self.font = font or settings.BUTTON_FONT
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.base_color = settings.RED
        self.hover_color = settings.GREEN
        self.disabled_color = settings.DARK_GRAY
        self.text_color = settings.WHITE

    def is_hovered_over(self) -> bool:
        return self.enabled and self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self) -> bool:
        return self.enabled and self.is_hovered_over() and pygame.mouse.get_pressed()[0]

    def handle_event(self, event) -> bool:
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def render(self, screen):
        color = self.disabled_color
        if self.enabled:
            color = self.hover_color if self.is_hovered_over() else self.base_color
        pygame.draw.rect(screen, color, self.rect, 0, 5)
        pygame.draw.rect(screen, settings.WHITE, self.rect, 2, 5)
        button_text = self.font.render(self.text, True, self.text_color)
        text_rect = button_text.get_rect(center=self.rect.center)
        screen.blit(button_text, text_rect)
