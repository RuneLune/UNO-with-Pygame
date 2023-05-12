from __future__ import annotations
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject
from player.player import Player
from game.game import Game
import util.colors as colors

import pygame
from overrides import overrides
from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class Space(GameObject, Observer):
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
        player: Type[Player] = None,
        game: Type[Game] = None,
    ):
        self.turn = False
        self.turn_color = colors.red
        self.player = player
        self.game = game
        super().__init__(surface, name, width, height, left, top, z_index)

    @overrides
    def start(self):
        self.color = colors.white
        self.rect_copy = pygame.rect.Rect((0, 0), self.rect.size)
        if self.turn is True:
            pygame.draw.rect(
                surface=self.image, color=self.turn_color, rect=self.rect_copy, width=2
            )
        else:
            pygame.draw.rect(
                surface=self.image, color=self.color, rect=self.rect_copy, width=2
            )

    @overrides
    def update(self):
        self.turn = self.player.is_turn()
        time_left = self.game.remain_turn_time()
        # 턴 시작하면 테두리 색 변화
        if self.turn is True:
            self.image.fill(colors.black)
            pygame.draw.rect(
                surface=self.image, color=self.turn_color, rect=self.rect_copy, width=5
            )
            pygame.draw.line(
                surface=self.image,
                color=colors.orange,
                start_pos=(
                    self.rect_copy.bottomleft[0] + 5,
                    self.rect_copy.bottomleft[1] - 13,
                ),
                end_pos=(
                    time_left * self.width / 10 - 5,
                    self.rect_copy.bottom - 13,
                ),
                width=15,
            )
        elif self.turn is False:
            self.image.fill(colors.black)
            pygame.draw.rect(
                surface=self.image, color=self.color, rect=self.rect_copy, width=3
            )
