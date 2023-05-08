from __future__ import annotations

import pygame

from card.cards import Cards
from gameobj.gameobj import GameObject
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class LastCard(GameObject):
    def __init__(
        self,
        surface: pygame.Surface,
        name: str = "lastcard",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1,
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index, key_index)
        self.cards_cls = Cards()

    def observer_update(self, subject: Type[Subject]):
        self.image = self.cards_cls.get_card_image(subject._discard_pile[0])
