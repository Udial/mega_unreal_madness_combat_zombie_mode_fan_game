import pygame as pg
from ..core import config as cfg


def menu_render(surface: pg.surface.Surface) -> None:
    surface.fill(cfg.BG_COLOR)
    