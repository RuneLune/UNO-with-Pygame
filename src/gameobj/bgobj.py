import pygame
from typing import Tuple

from .gameobj import GameObject
import util.colors as color

pygame.init()


class BackgroundObject(GameObject):
    def __init__(
        self,
        color: Tuple[int, int, int] = color.black,
        name: str = "BackgroundObject",
        z_index: int = -999,
    ) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self._color = color
        image = pygame.Surface(screen_rect.size)
        image.fill(self._color)
        return super(BackgroundObject, self).__init__(image, name, z_index=z_index)

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self._color = value
        self._image.fill(self._color)
        return None

    pass
