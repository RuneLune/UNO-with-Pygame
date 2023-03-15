import pygame


class Settings():
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.reset(self)
        return super().__init__(self)

    # Settings reset method
    def reset(self):
        # Screen size
        self.screen_size = (1280, 960)

        # Key bindings
        self.key_bindings.left = pygame.K_LEFT
        self.key_bindings.right = pygame.K_RIGHT
        self.key_bindings.up = pygame.K_UP
        self.key_bindings.down = pygame.K_DOWN
        self.key_bindings.select = pygame.K_RETURN
        self.key_bindings.cancel = pygame.K_ESCAPE

        # Colorblind mode
        self.colorblind_mode = False

        return self
