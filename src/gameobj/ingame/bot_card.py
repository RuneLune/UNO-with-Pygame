from __future__ import annotations

import pygame
from overrides import overrides
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject
from manager.cfgmgr import Config

from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject

# 봇이 드로우 하면 카드가 생성되고 이동
# 봇이 카드를 내면 버린 카드 더미로 이동
# 무조건 뒷면


class BotCard(GameObject, Observer):
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
        target_pos: tuple = (0, 0),
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index)

        self.draw_start = False
        self.draw_end = False

        self.discard_start = False
        self.discard_end = False

    def observer_update(self, subject: Type[Subject]):
        pass
