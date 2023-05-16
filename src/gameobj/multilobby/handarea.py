import pygame

from .areabg import AreaBackground
import util.colors as color


class HandArea(AreaBackground):
    def __init__(self):
        screen_rect = pygame.display.get_surface().get_rect()
        return super().__init__(
            pygame.Rect(
                0,
                screen_rect.height * 2 // 3,
                screen_rect.width * 3 // 4,
                screen_rect.height // 3,
            ),
            color.dark_olive_green,
            color.white,
            border_width=2,
        )

    pass
