from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as color


class MenuKey(TextObject):
    Inst_created: int = 0
    Insts: list[MenuKey] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        MenuKey.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.color = color.white
        self.text = self.text + " |"
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.topright = (
            screen_rect.width * 9 // 20,
            screen_rect.height * (2 + self.Inst_created) // 16,
        )
        return None

    @overrides
    def on_destroy(self) -> None:
        MenuKey.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in MenuKey.Insts:
            inst.on_destroy()
            del inst
            pass
        MenuKey.Inst_created = 0
        return None

    pass
