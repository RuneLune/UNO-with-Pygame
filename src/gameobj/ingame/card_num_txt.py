from overrides import overrides
import pygame
from typing import Tuple, Type
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
import util.colors as colors
from abstrclass.observer import Observer

from gameobj.txtobj import TextObject


class CardNumber(TextObject, Observer):
    def observer_update(self, subject: Type[Subject]) -> None:
        self.player = subject
        self.card_num = len(subject.get_hand_cards())

    @overrides
    def update(self) -> None:
        if self.card_num != len(self.player.get_hand_cards()):
            self.card_num = len(self.player.get_hand_cards())
            self.__init__(
                text=str(self.card_num),
                font=self.font,
                color=self.color,
                left=self.left,
                top=self.top,
                z_index=self.z_index,
            )
