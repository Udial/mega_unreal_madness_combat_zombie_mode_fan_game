import pygame
from ... import settings 


class Button():
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int, text: str, enabled: bool, screen=None):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.text = text
    
    def is_hovered_over(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if (self.x_pos < mouse_x < (self.x_pos + self.width)) and (self.y_pos < mouse_y < (self.y_pos + self.height)):
            return True
        else:
            return False
    
    def is_clicked(self) -> bool:
        if self.is_hovered_over() and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

    def render(self, screen):
        button_text = settings.BUTTON_FONT.render(self.text, True, settings.WHITE)
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos),(self.width, self.height))
        pygame.draw.rect(screen, settings.GREEN if self.is_hovered_over() else settings.RED, button_rect, 0, 5)
        screen.blit(button_text, (self.x_pos + 10, self.y_pos + 3))
        
