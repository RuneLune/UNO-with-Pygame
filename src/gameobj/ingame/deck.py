from __future__ import annotations

import pygame
from gameobj.gameobj import GameObject
import util.colors as colors
from overrides import overrides
import cv2
import numpy
from abstrclass.observer import Observer
from typing import Type, TYPE_CHECKING
from card.cards import Cards

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class Deck(GameObject, Observer):
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
        self.draw_flag = False
        self.user_turn = False
        self.rect_size = self.rect.size
        self.img_copy = self.image
        self.cards_cls = Cards()

    @overrides
    def on_mouse_enter(self) -> None:
        self.image = self.create_neon(self.image)

    @overrides
    def on_mouse_exit(self) -> None:
        self.image = self.img_copy

    @overrides
    def on_mouse_down(self) -> None:
        # 카드 드로우
        if self.user_turn is True:
            self.draw_flag = True

    def observer_update(self, subject: Type[Subject]):
        self.user = subject.get_user()
        self.user_turn = self.user.is_turn()

    @overrides
    def update(self) -> None:
        if self.user_turn is True:
            return None
        else:
            self.user_turn = self.user.is_turn()

    def create_neon(self, surf):
        surf_alpha = surf.convert_alpha()
        rgb = pygame.surfarray.array3d(surf_alpha)
        alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
        image = numpy.concatenate((rgb, alpha), 2)
        cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
        cv2.blur(image, ksize=(5, 5), dst=image)
        bloom_surf = pygame.image.frombuffer(
            image.flatten(), image.shape[1::-1], "RGBA"
        )
        bloom_surf = pygame.transform.rotate(bloom_surf, 90)
        bloom_surf = pygame.transform.flip(bloom_surf, True, False)
        return bloom_surf
