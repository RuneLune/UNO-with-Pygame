from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as color


class VolumeKey(TextObject):
    Inst_created: int = 0
    Insts: list[VolumeKey] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        VolumeKey.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 32
        )
        self.color = color.white
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            screen_rect.width * (13 + self.Inst_created) // 17,
            screen_rect.height * 3 // 4,
        )
        return None

    @overrides
    def on_destroy(self) -> None:
        VolumeKey.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in VolumeKey.Insts:
            inst.on_destroy()
            del inst
            pass
        VolumeKey.Inst_created = 0
        return None

    pass
