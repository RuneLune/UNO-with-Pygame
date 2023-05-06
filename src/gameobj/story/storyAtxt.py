from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
from metaclass.singleton import SingletonMeta
import util.colors as color


class StoryAText(TextObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.text = "A: 첫 분배 시 컴퓨터 플레이어에게 기술 카드를 50% 더 높은 확률로 분배"
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self.color = color.white
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.z_index = 997
        self._visible = False
        return None

    pass
