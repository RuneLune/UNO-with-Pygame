from __future__ import annotations

from overrides import overrides
import pygame

from manager.cfgmgr import Config
from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as color


class KeyBind(TextObject):
    Inst_created: int = 0
    Insts: list[KeyBind] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        KeyBind.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        config = Config().config.get("keybindings")
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.color = color.black
        self.target_config_key = self.text.lower()
        self.text = (
            f"{self.text}: {pygame.key.name(config.get(self.target_config_key))}"
        )
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.bottomleft = (
            screen_rect.width // 25,
            screen_rect.height * (12 + self.Inst_created) // 19,
        )
        return None

    @overrides
    def on_destroy(self) -> None:
        KeyBind.Insts.remove(self)
        KeyBind.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in KeyBind.Insts:
            inst.on_destroy()
            del inst
            pass
        KeyBind.Inst_created = 0
        return None

    pass
