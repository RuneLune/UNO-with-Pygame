from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
from metaclass.singleton import SingletonMeta
import util.colors as color


class BotDText(TextObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.text = "D: 유저 드로우 시 1장이 아닌 2장 드로우"
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self.color = color.black
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.z_index = 2000
        self._visible = False
        self.disable()
        return None

    pass
