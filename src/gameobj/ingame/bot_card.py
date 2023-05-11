from __future__ import annotations

import pygame
from overrides import overrides
from abstrclass.subject import Subject

from gameobj.gameobj import GameObject
from manager.cfgmgr import Config
from card.cards import Cards

from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from abstrclass.subject import Subject

# 봇이 드로우 하면 카드가 생성되고 이동
# 봇이 카드를 내면 버린 카드 더미로 이동
# 무조건 뒷면


class BotCard(GameObject, Observer):
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
        target_pos: tuple = (0, 0),
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index)
        screen_size = Config().get_screen_resolution()
        card_size = self.rect.size
        self.card_cls = Cards()

        self.draw_start = False
        self.draw_end = False

        self.discard_start = False
        self.discard_end = False

        self.target_pos = target_pos
        self.draw_pile_pos = (
            screen_size[0] * (3 / 8) - card_size[0] + 1,
            screen_size[1] * (1 / 3) - card_size[1] / 2 + 1,
        )
        self.discard_pile_pos = (
            screen_size[0] * 3 / 8 + card_size[0],
            screen_size[1] * 1 / 3 - card_size[1] / 2,
        )
        self.vec_target = pygame.Vector2(self.target_pos)
        self.vec_rect = pygame.Vector2((self.rect.x, self.rect.y))
        self.move_rate = (self.vec_target - self.vec_rect).normalize() * 20

    def observer_update(self, subject: Type[Subject]):
        self.image = self.card_cls.get_card_image(subject._discard_pile[0])

    @overrides
    def update(self):
        if self.discard_start is True:
            if self.vec_rect[0] < self.target_pos[0]:
                self.rect.x = self.target_pos[0]
                self.rect.y = self.target_pos[1]
                self.discard_start = False
                self.discard_end = True
            else:
                self.vec_rect += self.move_rate
                self.rect.x = self.vec_rect[0]
                self.rect.y = self.vec_rect[1]

        # 카드 뽑기 애니메이션
        if self.draw_start is True:
            if self.vec_rect.x > self.target_pos[0]:
                self.rect.x = self.target_pos[0]
                self.rect.y = self.target_pos[1]
                self.draw_start = False
                self.draw_end = True
                self.target_pos = self.discard_pile_pos
                self.move_rate = (self.vec_target - self.vec_rect).normalize() * 20
            else:
                self.vec_rect += self.move_rate
                self.rect.x = self.vec_rect[0]
                self.rect.y = self.vec_rect[1]
