import pygame
from ..entities.bullet import Bullet


class CombatSystem:
    def __init__(self, entitities: list):
        self.entities = entitities

    def handle_player_shoot(self, player, input_state):
        weapon = player.weapon

        if input_state.shoot and weapon.can_shoot():
            weapon.shoot()

            direction = self.get_direction(player)

            bullet = Bullet(
                player.rect.centerx,
                player.rect.centery,
                direction,
                weapon.damage
            )

            self.entities.append(bullet)
            print('hui')

    def get_direction(self, player):
        mos_pos = pygame.mouse.get_pos()

        direction = pygame.Vector2(
            mos_pos[0] - player.rect.centerx,
            mos_pos[1] - player.rect.centery
            )
        
        if direction.length() > 0:
            direction = direction.normalize()

        return direction
    
    def process_bullets(self, bullets: list, zombies: list, damage_system):
        for bullet in bullets:
            for zombie in zombies:
                if bullet.rect.colliderect(zombie.rect):
                    damage_system.apply_damage(zombie, bullet.damage)
                    bullet.is_alive = False