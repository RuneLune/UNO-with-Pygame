import pygame

from .areabg import AreaBackground

# import util.colors as color


class TableArea(AreaBackground):
    def __init__(self):
        screen_rect = pygame.display.get_surface().get_rect()
        return super().__init__(
            pygame.Rect(0, 0, screen_rect.width * 3 // 4, screen_rect.height * 2 // 3),
            (0, 150, 100),
        )

    pass
