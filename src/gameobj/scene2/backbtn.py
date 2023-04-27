from __future__ import annotations

from overrides import overrides
import pygame

from ..txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as colors


class BackButton(TextObject):
    def __init__(self) -> None:
        return super(BackButton, self).__init__(
            "Back to Previous Scene",
            pygame.font.Font(font_resource("MainFont.ttf"), 30),
            colors.white,
            "Scene2_BackButton",
            -1,
            -1,
            10,
            10,
            999,
        )

    @overrides
    def on_mouse_enter(self) -> None:
        self.image = self.font.render(self.text, True, colors.red)
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        self.image = self.font.render(self.text, True, self.color)
        return None

    pass
