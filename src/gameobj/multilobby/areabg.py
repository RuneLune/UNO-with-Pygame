import pygame
from typing import Tuple

from ..gameobj import GameObject
import util.colors as color

pygame.init()


class AreaBackground(GameObject):
    def __init__(
        self,
        area_rect: pygame.Rect = None,
        color: Tuple[int, int, int] = color.black,
        border_color: Tuple[int, int, int] = color.white,
        border_width: int = 0,
        name: str = "AreaBackground",
        z_index: int = -998,
        screen: pygame.Surface = None,
    ) -> None:
        if screen is None:
            screen_rect = pygame.display.get_surface().get_rect()
            pass
        else:
            screen_rect = screen.get_rect()
            pass
        if area_rect is None:
            area_rect = screen_rect
            pass
        self._area_rect = area_rect
        self._color = color
        self._border_color = border_color
        self._border_width = border_width
        self.image = pygame.Surface(area_rect.size)
        self.image.fill(self._color)
        self.draw_border()
        return super(AreaBackground, self).__init__(
            self.image,
            name,
            z_index=z_index,
            screen=screen,
            left=area_rect.left,
            top=area_rect.top,
        )

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self._color = value
        self.image.fill(self._color)
        self.draw_border()
        return None

    def draw_border(self) -> None:
        if self._border_width > 0:
            pygame.draw.rect(
                self.image,
                self._border_color,
                self.image.get_rect(),
                self._border_width,
            )
            pass
        return None

    pass
