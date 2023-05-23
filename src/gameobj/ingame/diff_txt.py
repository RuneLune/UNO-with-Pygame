from overrides import overrides
import pygame
from typing import Tuple, Type
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
import util.colors as colors
from abstrclass.observer import Observer

from gameobj.txtobj import TextObject


class DiffNumber(TextObject, Observer):
    @overrides
    def start(self) -> None:
        pass

    def observer_update(self, subject: Type[Subject]) -> None:
        self.player = subject
        self.card_num = len(self.player.get_hand_cards())
        self.fps = 60
        self.time_count = self.fps * 2
        self._visible = False

    @overrides
    def update(self) -> None:
        if self.card_num != len(self.player.get_hand_cards()):
            self.diff = len(self.player.get_hand_cards()) - self.card_num
            self.card_num = len(self.player.get_hand_cards())
            if self.diff > 0:
                self._visible = True
                self.__init__(
                    text="+" + str(self.diff),
                    font=self.font,
                    color=self.color,
                    left=self.left,
                    top=self.top,
                    z_index=self.z_index,
                )
        if self._visible is True:
            if self.time_count > 0:
                self.time_count -= 1
            else:
                self._visible = False
                self.time_count = self.fps * 1.5
