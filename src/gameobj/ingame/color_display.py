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


class ColorDisplay(GameObject, Observer):
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
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index, key_index)
        self.color = colors.white

    def observer_update(self, subject: Type[Subject]):
        discard_card = subject.get_discard_info().get("discarded_card")
        current_color = discard_card.get("color")

        if current_color == "wild":
            self.color = colors.black
        elif current_color == "red":
            self.color = colors.red
        elif current_color == "blue":
            self.color = colors.blue
        elif current_color == "green":
            self.color = colors.green
        elif current_color == "yellow":
            self.color = colors.yellow

    @overrides
    def update(self):
        pygame.draw.circle(
            self.image,
            color=self.color,
            center=self.rect.center,
            radius=self.height / 2,
            width=25,
        )
