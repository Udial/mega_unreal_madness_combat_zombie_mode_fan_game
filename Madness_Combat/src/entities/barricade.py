import pygame
from .base_entity import BaseEntity
from ..utils.geometry import make_entry_barricade_rect, make_wall_entry
from ... import settings


class Barricade(BaseEntity):
    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.points = self._make_points(entry_point)

        x, y, width, height = self._get_bounding_rect(self.points)
        super().__init__(int(x), int(y), int(width), int(height))
        self.armor = 0
        self.hp = 50
        self.max_hp = self.hp
        self.level = 1
        self.sprite = self._load_sprite()

    def _make_points(self, entry_point):
        return make_wall_entry(
            entry_point.points, u1=0, u2=1, v_top=0.35, v_bottom=0.65
        )

    def _get_bounding_rect(self, points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return min_x, min_y, max_x - min_x, max_y - min_y

    def _load_sprite(self):
        if getattr(self.entry_point, "type", "top") in ("left", "right"):
            return None

        try:
            sprite = pygame.image.load(settings.BARRICADE_SPRITE_PATH).convert_alpha()
            return pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
        except Exception:
            return None

    def _camera_points(self, camera):
        if camera is None:
            return self.points
        return camera.apply_points(self.points)

    def render(self, screen, camera=None):
        if self.entry_point.type not in ("left, right"):
            rect = self.rect
            if camera is not None:
                rect = camera.apply(self.rect)
            pygame.draw.rect(screen, settings.WOOD_COLOR, rect, 0)
            pygame.draw.rect(screen, settings.BLACK, rect, 2)
            return

        points = self._camera_points(camera)
        pygame.draw.polygon(screen, settings.WOOD_COLOR, points, 0)
        pygame.draw.polygon(screen, settings.BLACK, points, 2)
