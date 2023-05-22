from __future__ import annotations

import pygame
from overrides import overrides

from gameobj.gameobj import GameObject
from manager.cfgmgr import Config
from manager.soundmgr import SoundManager

from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class Card(GameObject, Observer):
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
        code: int = -1,
        target_pos: tuple = (0, 0),
        index: int = -1,
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index)
        self.left = left
        self.top = top
        self.target_pos = target_pos
        self.code = code
        self.index = index

        self.user = False
        self.user_turn = False

        self.discard_start = False
        self.discard_end = False

        self.draw_start = False
        self.draw_end = False

        self.playable = False
        self.enter = False

        settings = Config()
        screen_size = settings.get_screen_resolution()

        card_size = self.rect.size

        self.discard_pile_pos = (
            screen_size[0] * 3 / 8 + card_size[0],
            screen_size[1] * 1 / 3 - card_size[1] / 2,
        )
        self.draw_pile_pos = (
            screen_size[0] * (3 / 8) - card_size[0] + 1,
            screen_size[1] * (1 / 3) - card_size[1] / 2 + 1,
        )
        self.user_card_pos = [
            (
                (i + 1) * card_size[0],
                screen_size[1] * (2 / 3) + card_size[1] / 2,
            )
            if i < 10
            else (
                (i - 9) * card_size[0],
                screen_size[1] * (2 / 3) + card_size[1] * 3 / 2,
            )
            for i in range(30)
        ]

        self.vec_target = pygame.Vector2(self.target_pos)
        self.vec_rect = pygame.Vector2((self.rect.x, self.rect.y))
        self.move_rate = (self.vec_target - self.vec_rect).normalize() * 40

    @overrides
    def on_mouse_enter(self) -> True:
        if self.user_turn is True and self.playable is True:
            self.rect.y -= 10
            self.enter = True
        else:
            self.enter = False

    @overrides
    def on_mouse_exit(self) -> None:
        if self.enter is True:
            self.rect.y += 10

    @overrides
    def on_mouse_down(self) -> None:
        if self.user_turn is True and self.playable is True:
            self.discard_start = True
            SoundManager().play_effect("discard")

        else:
            self.discard_start = False

    def position_update(self, subject: Type[Subject], index):
        # 카드 위치 재정렬
        if self.user is True:
            self.index = index
            self.rect.x = self.user_card_pos[self.index][0]
            self.rect.y = self.user_card_pos[self.index][1]

    def turn_update(self, subject: Type[Subject]):
        self.user_turn = subject.get_user().is_turn()
        # 유저턴이면 낼수 있는 카드인지 확인
        if self.user_turn is True:
            discardable_cards = subject.get_user().get_discardable_cards_index()
            if self.index in discardable_cards:
                self.playable = True
            else:
                self.playable = False

    @overrides
    def update(self) -> None:
        # 카드 내기 애니메이션
        if self.discard_start is True:
            if self.vec_rect[1] > self.target_pos[1]:
                self.vec_rect += self.move_rate
                self.rect.x = self.vec_rect[0]
                self.rect.y = self.vec_rect[1]
            else:
                self.rect.x = self.discard_pile_pos[0]
                self.rect.y = self.discard_pile_pos[1]
                self.discard_start = False
                self.discard_end = True

        # 카드 뽑기 애니메이션
        if self.draw_start is True:
            if self.vec_rect.y > self.target_pos[1]:
                self.rect.x = self.target_pos[0]
                self.rect.y = self.target_pos[1]
                self.draw_start = False
                self.draw_end = True
                self.target_pos = self.discard_pile_pos
                self.vec_target = pygame.Vector2(self.target_pos)
                self.move_rate = (self.vec_target - self.vec_rect).normalize() * 40
            else:
                self.vec_rect += self.move_rate
                self.rect.x = self.vec_rect[0]
                self.rect.y = self.vec_rect[1]
