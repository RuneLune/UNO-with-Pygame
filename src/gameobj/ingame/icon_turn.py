from __future__ import annotations
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject

import pygame
from overrides import overrides
from abstrclass.observer import Observer
from manager.cfgmgr import Config
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class TurnIcon(GameObject, Observer):
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
        key_index: int = -1,
        screen: pygame.Surface = None,
    ) -> None:
        super().__init__(
            surface, name, width, height, left, top, z_index, key_index, screen
        )

    @overrides
    def start(self) -> None:
        self.left = -self.width

    def observer_update(self, subject: Type[Subject]):
        self.user = subject

    @overrides
    def update(self) -> None:
        if self.user.is_turn() is True:
            self._visible = True
            if self.left < 0:
                self.left += 1
        else:
            self._visible = False
