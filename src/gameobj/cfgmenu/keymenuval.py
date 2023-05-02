from __future__ import annotations

from overrides import overrides
import pygame

from manager.cfgmgr import Config
from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as color


class KeyMenuValue(TextObject):
    Inst_created: int = 0
    Insts: list[KeyMenuValue] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        KeyMenuValue.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        config = Config().config.get("keybindings")
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.color = color.white
        self.target_config_key = self.text
        self.text = pygame.key.name(config.get(self.target_config_key))
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.midtop = (
            screen_rect.width * 5 // 8,
            screen_rect.height * (6 + self.Inst_created) // 16,
        )
        return None

    @overrides
    def on_destroy(self) -> None:
        KeyMenuValue.Insts.remove(self)
        KeyMenuValue.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in KeyMenuValue.Insts:
            inst.on_destroy()
            del inst
            pass
        KeyMenuValue.Inst_created = 0
        return None

    def keybind_start(self) -> None:
        self.color = color.red
        self.image = self.font.render(self.text, True, self.color)
        return None

    def keybind_end(self) -> None:
        self.color = color.white
        self.text = pygame.key.name(
            Config().config.get("keybindings").get(self.target_config_key)
        )
        self.image = self.font.render(self.text, True, self.color)
        return None

    pass
