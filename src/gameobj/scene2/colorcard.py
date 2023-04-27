import pygame
from overrides import overrides
from typing import Tuple

from gameobj.gameobj import GameObject
import util.colors as color


class ColorCard(GameObject):
    @overrides
    def start(self) -> None:
        self._color = color.white
        self.image.fill(self._color)
        return None

    @overrides
    def on_mouse_drag(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0] - self.mouse_gap[0]
        self.rect.y = mouse_pos[1] - self.mouse_gap[1]
        return None

    @overrides
    def on_mouse_down(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.prev_z_index = self.z_index
        self.z_index = 999
        self.mouse_gap = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        return None

    @overrides
    def on_mouse_up(self) -> None:
        self.z_index = self.prev_z_index
        self.mouse_gap = None
        return None

    @overrides
    def on_mouse_enter(self) -> None:
        self.rect_y_move += 1
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        self.rect_y_move -= 1
        return None

    @overrides
    def start(self) -> None:
        self.rect_y_move = 0

    @overrides
    def update(self) -> None:
        if self.rect_y_move < 0:
            self.rect.move_ip(0, 5)
            self.rect_y_move += 1
            pass
        elif self.rect_y_move > 0:
            self.rect.move_ip(0, -5)
            self.rect_y_move -= 1
            pass
        return None

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self._color = value
        self.image.fill(self._color)
        return None

    pass
