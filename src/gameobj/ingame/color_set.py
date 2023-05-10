from __future__ import annotations
from overrides import overrides

import pygame
from abstrclass.subject import Subject
from gameobj.gameobj import GameObject
import util.colors as colors
from manager.cfgmgr import Config
from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class ColorSet(GameObject, Observer):
    @overrides
    def __init__(
        self,
        surface: pygame.surface,
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1,
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index, key_index)

    def observer_update(self, subject: Type[Subject]):
        pass

    @overrides
    def update(self):
        pass