import pygame
from .collision_system import CollisionSystem


class MovementSystem:
    def __init__(self, collision_system):
        self.collision_system = collision_system

    def update(self, entity , input_state, dt):
        direction = input_state.move

        if direction.length() > 0:
            direction = direction.normalize()

        entity.velocity = direction * entity.speed

        prev_x = entity.pos_x
        entity.pos_x += entity.velocity.x * dt
        entity.update_rect()
        
        if self.collision_system.check_if_player_point_is_beyond_wall_horizontal(entity.rect):
            entity.pos_x = prev_x
            entity.update_rect()

        prev_y = entity.pos_y
        entity.pos_y += entity.velocity.y * dt
        entity.update_rect()

        if self.collision_system.check_if_player_point_is_beyond_wall_horizontal(entity.rect):
            entity.pos_y = prev_y
            entity.update_rect()
        
        if self.collision_system.check_if_player_point_is_beyond_wall_vertical(entity.rect):
            entity.pos_y = prev_y
            entity.update_rect()