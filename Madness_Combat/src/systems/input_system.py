import pygame

class InputState:
    def __init__(self):
        self.move = pygame.Vector2(0, 0)
        self.shoot = False
        self.interact = False
        self.buying_barricade = False
        self.buying_ammo = False
        self.buying_medkit = False

class InputSystem:

    last_keys = None

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
        if keys[pygame.K_e]:
            input_state.interact = True
        else:
            input_state.interact = False
        if keys[pygame.K_F1] and not InputSystem.last_keys[pygame.K_F1]:
            input_state.buying_barricade = True
        else:
            input_state.buying_barricade = False
        
        InputSystem.last_keys = keys

        mouse_buttons = pygame.mouse.get_pressed()
        input_state.shoot = mouse_buttons[0]

        return input_state