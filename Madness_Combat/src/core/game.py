import pygame
import sys
from ... import settings


def is_running_handler() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True
    

def run():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.WINDOW_NAME)
    pygame.time.Clock().tick(settings.FPS)
    clock = pygame.time.Clock().tick(settings.FPS)
    running = True

    while running:
        running = is_running_handler()
        dt = clock / 1000
        screen.fill(settings.GRAY_COLOR_TEMP)
        pygame.display.flip()

    pygame.quit()
    sys.exit()