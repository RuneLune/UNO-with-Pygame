from overrides import overrides
from typing import Tuple
import pygame

from .txtobj import TextObject
import util.colors as colors

pygame.init()


class TextButtonObject(TextObject):
    highlighting_color = colors.gray

    @overrides
    def on_mouse_enter(self) -> None:
        self.image = self.font.render(self.text, True, self.highlighting_color)
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        self.image = self.font.render(self.text, True, self.color)
        return None

    @overrides
    def on_mouse_up_as_button(self) -> None:
        self.on_click()
        return None

    def change_highlighting_color(self, color: Tuple[int, int, int]) -> None:
        self.highlighting_color = color
        return None

    def on_click(self) -> None:
        return None

    pass
