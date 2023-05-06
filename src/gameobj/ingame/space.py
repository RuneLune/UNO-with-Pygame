from __future__ import annotations

from gameobj.gameobj import GameObject
import util.colors as colors

# from typing import Type
import pygame
from overrides import overrides

# from abstrclass.observer import Observer


class Space(GameObject):
    @overrides
    def __init__(
        self,
        surface: pygame.Surface,
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        color: tuple = colors.black,
    ) -> None:
        self.turn = False
        self.color = color
        self.turn_color = colors.red
        super().__init__(surface, name, width, height, left, top, z_index)

    @overrides
    def start(self) -> None:
        self.border = pygame.rect.Rect((0, 0), self.rect.size)
        if self.turn is True:
            pygame.draw.rect(
                surface=self.image, color=self.turn_color, rect=self.border, width=2
            )
        else:
            pygame.draw.rect(
                surface=self.image, color=colors.white, rect=self.border, width=2
            )

    @overrides
    def update(self):
        # 턴 시작하면 테두리 색 변화
        if self.turn is True:
            pygame.draw.rect(
                surface=self.image, color=self.turn_color, rect=self.border, width=2
            )
        else:
            pygame.draw.rect(
                surface=self.image, color=colors.white, rect=self.border, width=2
            )
