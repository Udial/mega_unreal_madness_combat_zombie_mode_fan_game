import pygame

class MovementSystem:
    def update(self, entity, input_state, dt):
        direction = input_state.move

        if direction.length() > 0:
            direction = direction.normalize()

        entity.velocity = direction * entity.speed

        entity.pos_x += entity.velocity.x * dt
        entity.pos_y += entity.velocity.y *dt

        entity.rect.topleft = (entity.pos_x, entity.pos_y)