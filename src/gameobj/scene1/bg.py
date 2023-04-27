from __future__ import annotations

import pygame

from ..gameobj import GameObject
import util.colors as colors


class Background(GameObject):
    def __init__(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        background = pygame.Surface(screen_rect.size)
        background.fill(colors.gray)
        return super(Background, self).__init__(
            background, "Scene1_Background", z_index=-999
        )

    pass
