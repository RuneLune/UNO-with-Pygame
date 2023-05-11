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
        color: tuple = (0, 0, 0),
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index, key_index)
        self.user = None
        self.color = color
        self.rect_copy = pygame.rect.Rect((0, 0), self.rect.size)
        if self.color == colors.red:
            self.choice = "red"
        elif self.color == colors.green:
            self.choice = "green"
        elif self.color == colors.blue:
            self.choice = "blue"
        elif self.color == colors.yellow:
            self.choice = "yellow"
        else:
            self.choice = "black"

    @overrides
    def start(self):
        self._visible = False

    @overrides
    def on_mouse_down(self):
        self.user.set_color(self.choice)
        self._visible = False

    def user_update(self, subject: Type[Subject]):
        self.user = subject.get_user()

    def observer_update(self, subject: Type[Subject]):
        # 유저가 와일드 카드를 내서 색을 선택해야 하는 상황 감지
        if self.user.is_turn() is True and self.user._discarded_wild is True:
            self._visible = True

    @overrides
    def update(self):
        # 모서리 곡률 추가
        pygame.draw.rect(
            surface=self.image, color=self.color, rect=self.rect_copy, border_radius=4
        )
        pass
