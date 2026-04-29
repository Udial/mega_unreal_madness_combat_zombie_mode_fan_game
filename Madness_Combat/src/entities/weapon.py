import pygame


class LongRangeWeapon:
    def __init__(self):
        self.damage = 20
        self.cooldown = 0
        self.fire_rate = 0.3

    def uptade(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt
    
    def can_shoot(self):
        return self.cooldown <= 0
    
    def shoot(self):
        self.cooldown = self.fire_rate