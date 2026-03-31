import pygame as pg
import sys
from . import config as cfg
from ..renderer import menu_renderer


def handle_events() -> bool:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True


def run() -> None:
    pg.init()
    screen = cfg.SCREEN_RESOLUTION
    pg.display.set_caption('Madness Combat: Zombies!')
    cfg.CLOCK.tick(cfg.FPS)
    running = True

    while running:
        running = handle_events()
        menu_renderer.menu_render(screen)
        pg.display.flip()

    
    pg.quit()
    sys.exit()