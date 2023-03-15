import pygame


class Settings():
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.reset()
        return super().__init__()

    # Settings reset method
    def reset(self):
        # Screen size
        self.screen_size = (1280, 960)

        # Key bindings
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_select = pygame.K_RETURN
        self.key_cancel = pygame.K_ESCAPE

        # Colorblind mode
        self.colorblind_mode = False

        return self
