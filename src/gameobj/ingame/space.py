from __future__ import annotations

from gameobj.gameobj import GameObject
import util.colors as colors
from typing import Type
import pygame
from overrides import overrides

from abstrclass.observer import Observer


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
        self.turn_color = colors.alice_blue
        super().__init__(surface, name, width, height, left, top, z_index)

    @overrides
    def update(self):
        # 턴 시작하면 테두리 색 변화
        if self.turn is True:
            self.rect = pygame.draw.rect(
                self.image, color=self.turn_color, rect=self.rect, width=2
            )
        else:
            self.rect = pygame.draw.rect(
                self.image, color=colors.white, rect=self.rect, width=2
            )

    # def update(self, subject: Type[Subject]):
    #     self.turn = subject.get_user().is_turn()
    #     pass
