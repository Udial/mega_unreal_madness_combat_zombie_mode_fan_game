import pygame


class InputState:
    def __init__(self):
        self.move = pygame.Vector2(0, 0)
        self.shoot = False
        self.shoot_pressed = False
        self.interact = False
        self.interact_pressed = False
        self.buying_barricade = False
        self.buying_ammo = False
        self.buying_medkit = False
        self.reloading_weapon = False
        self.starting_wave = False
        self.pause_pressed = False


class InputSystem:
    def __init__(self):
        self.last_keys = None
        self.last_mouse_buttons = None

    def get_input(self) -> object:
        input_state = InputState()
        keys = pygame.key.get_pressed()

        if self.last_keys is None:
            self.last_keys = keys

        if keys[pygame.K_w]:
            input_state.move.y = -1
        if keys[pygame.K_s]:
            input_state.move.y = 1
        if keys[pygame.K_a]:
            input_state.move.x = -1
        if keys[pygame.K_d]:
            input_state.move.x = 1
        input_state.interact = keys[pygame.K_e]
        input_state.interact_pressed = (
            keys[pygame.K_e] and not self.last_keys[pygame.K_e]
        )
        if keys[pygame.K_F1] and not self.last_keys[pygame.K_F1]:
            input_state.buying_barricade = True
        else:
            input_state.buying_barricade = False
        if keys[pygame.K_r]:
            input_state.reloading_weapon = True
        else:
            input_state.reloading_weapon = False
        if keys[pygame.K_TAB]:
            input_state.starting_wave = True
        else:
            input_state.starting_wave = False
        if keys[pygame.K_ESCAPE] and not self.last_keys[pygame.K_ESCAPE]:
            input_state.pause_pressed = True
        else:
            input_state.pause_pressed = False

        self.last_keys = keys

        mouse_buttons = pygame.mouse.get_pressed()

        if self.last_mouse_buttons is None:
            self.last_mouse_buttons = mouse_buttons

        input_state.shoot = mouse_buttons[0]

        if mouse_buttons[0] and not self.last_mouse_buttons[0]:
            input_state.shoot_pressed = True
        else:
            input_state.shoot_pressed = False

        self.last_mouse_buttons = mouse_buttons
        return input_state
