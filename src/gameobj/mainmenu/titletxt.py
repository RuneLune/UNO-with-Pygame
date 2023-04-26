from __future__ import annotations

from overrides import overrides
import pygame

from ..textobj import TextObject
from util.resource_manager import font_resource
import util.colors as colors


class TitleText(TextObject):
    def __init__(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        return super(TitleText, self).__init__(
            "UNO",
            pygame.font.Font(font_resource("MainFont.ttf"), screen_rect.height // 3),
            colors.black,
            "MainMenu_TitleText",
            -1,
            -1,
            10,
            10,
            999,
        )

    @overrides
    def start(self) -> None:
        screen_rect = self._screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.height * 3 // 10
        return None

    pass
