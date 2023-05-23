from __future__ import annotations
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject

import pygame
from overrides import overrides
from abstrclass.observer import Observer
from manager.cfgmgr import Config
from typing import Type, TYPE_CHECKING
from util.resource_manager import image_resource

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class SkipIcon(GameObject, Observer):
    @overrides
    def __init__(
        self,
        surface: pygame.Surface = pygame.image.load(image_resource("skipped.png")),
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1,
        screen: pygame.Surface = None,
    ) -> None:
        self.fps = 60
        self.time_count = self.fps * 2
        super().__init__(
            surface, name, width, height, left, top, z_index, key_index, screen
        )
        self._visible = False

    @overrides
    def update(self) -> None:
        if self._visible is True:
            if self.time_count > 0:
                self.time_count -= 1
            else:
                self._visible = False
                self.time_count = self.fps * 2
