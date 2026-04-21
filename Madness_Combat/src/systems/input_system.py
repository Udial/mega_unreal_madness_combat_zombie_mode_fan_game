import pygame

class InputState:
    def __init__(self):
        self.move = pygame.Vector2(0, 0)
        self.shoot = False

class InputSystem:
    def get_input(self) -> object:
        input_state = InputState()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            input_state.move.y = -1
        if keys[pygame.K_s]:
            input_state.move.y = 1
        if keys[pygame.K_a]:
            input_state.move.x = -1
        if keys[pygame.K_d]:
            input_state.move.x = 1
        
        mouse_buttons = pygame.mouse.get_pressed()
        input_state.shoot = mouse_buttons[0]

        return input_state