from __future__ import annotations
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject
import util.colors as colors

import pygame
from overrides import overrides
from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class UnoBtn(GameObject, Observer):
    @overrides
    def __init__(
        self,
        surface: pygame.Surface,
        name: str = "uno_button",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1,
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index, key_index)
        self.uno = False

    @overrides
    def start(self) -> None:
        self.uno_img = pygame.image.load("./res/img/uno.png")
        self.uno_img = pygame.transform.scale(self.uno_img, (self.width, self.height))
        self.uno_gray_img = pygame.transform.grayscale(self.uno_img)
        self.image = self.uno_gray_img

    def observer_update(self, subject: Type[Subject]):
        self.player = subject

    @overrides
    def on_mouse_down(self) -> None:
        if self.player.is_uno() is False:
            self.image = self.uno_img
            self.player.yell_uno()
            self.uno = True

    @overrides
    def on_mouse_enter(self) -> None:
        if self.uno is False:
            self.image = self.uno_img

    @overrides
    def on_mouse_exit(self) -> None:
        if self.uno is False:
            self.image = self.uno_gray_img

    @overrides
    def update(self) -> None:
        pass
