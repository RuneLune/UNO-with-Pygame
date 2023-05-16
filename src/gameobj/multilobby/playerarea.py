from __future__ import annotations

from typing import List
from overrides import overrides
import pygame

from gameobj.gameobj import GameObject
import util.colors as color


class PlayerArea(GameObject):
    Inst_created = 0
    Insts: List[PlayerArea] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        PlayerArea.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface((screen_rect.width // 4, screen_rect.height // 5))
        self.image.fill(color.black)
        self.draw_border()
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            screen_rect.width * 3 // 4,
            screen_rect.height // 5 * (PlayerArea.Inst_created - 1),
        )
        self.z_index = 100
        return None

    def draw_border(self) -> None:
        pygame.draw.rect(
            self.image, color.white, pygame.Rect((0, 0), self.image.get_rect().size), 2
        )
        return None

    def draw_text(self) -> None:
        return None

    @overrides
    def on_destroy(self) -> None:
        PlayerArea.Insts.remove(self)
        PlayerArea.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in PlayerArea.Insts:
            inst.on_destroy()
            del inst
            pass
        PlayerArea.Inst_created = 0
        return None

    pass
