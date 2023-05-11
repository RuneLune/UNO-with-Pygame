import pygame
from typing import Optional
from overrides import overrides

from .gameobj import GameObject
import util.colors as color

pygame.init()


class BarObject(GameObject):
    @overrides
    def __init__(
        self,
        min_value: int = 0,
        max_value: int = 100,
        value: int = 50,
        vertical: bool = False,
        background_color: Optional[tuple] = color.dark_gray,
        cover_color: Optional[tuple] = color.light_gray,
        name: str = "BarObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1,
    ) -> None:
        self._min_value = min_value
        self._max_value = max_value
        self._value = value
        self._vertical = vertical
        self._background_color = background_color
        self._cover_color = cover_color
        self._width = width if width >= 0 else 16 if vertical else 256
        self._height = height if height >= 0 else 256 if vertical else 16
        surface = pygame.Surface((self._width, self._height))
        return super().__init__(
            surface, name, width, height, left, top, z_index, key_index
        )

    @overrides
    def on_mouse_down(self) -> None:
        self.calc_value_from_mouse()
        return None

    @overrides
    def on_mouse_drag(self) -> None:
        self.calc_value_from_mouse()
        return None

    def calc_value_from_mouse(self) -> None:
        if self._vertical:
            mouse_pos = (
                self.rect.bottom - pygame.mouse.get_pos()[1]
            ) / self.rect.height
            pass
        else:
            mouse_pos = (pygame.mouse.get_pos()[0] - self.rect.left) / self.rect.width
            pass
        self._value = int(
            (self._max_value - self._min_value) * mouse_pos + self._min_value
        )
        if self._value < self._min_value:
            self._value = self._min_value
            pass
        elif self._value > self._max_value:
            self._value = self._max_value
            pass
        self._draw_bar()
        self.on_bar_move()
        return None

    def on_bar_move(self) -> None:
        pass

    def _draw_bar(self) -> None:
        print(self.image.get_size())
        self.image.fill(self._background_color)
        if self._vertical:
            bar_surface = pygame.Surface(
                (
                    self._width,
                    self._height
                    * (self._value - self._min_value)
                    / (self._max_value - self._min_value),
                )
            )
            bar_surface.fill(self._cover_color)
            self.image.blit(
                bar_surface, (0, self.image.get_height() - bar_surface.get_height())
            )
            pass
        else:
            bar_surface = pygame.Surface(
                self._width
                * (self._value - self._min_value)
                / (self._max_value - self._min_value),
                self._height,
            )
            bar_surface.fill(self._cover_color)
            self.image.blit(bar_surface, (0, 0))
            pass
        return None

    pass
