import pygame


class DamageSystem:
    def apply_damage(self, target, damage):
        target.hp -= damage

        if target.hp <= 0:
            target.is_alive = False