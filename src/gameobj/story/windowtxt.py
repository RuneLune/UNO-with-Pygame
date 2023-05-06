from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as color


class WindowText(TextObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 12
        )
        self.color = color.black
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.z_index = 999
        self._visible = False
        return None

    pass
