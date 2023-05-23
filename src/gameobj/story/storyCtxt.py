from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
from metaclass.singleton import SingletonMeta
import util.colors as color


class StoryCText(TextObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.text = "C: 2명의 컴퓨터 플레이어와 대전 / 매 5턴마다 낼 수 있는 카드 색상 무작위 변경"
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self.color = color.black
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.z_index = 997
        self._visible = False
        return None

    pass
