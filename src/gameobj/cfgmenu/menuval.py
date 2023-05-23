from __future__ import annotations

from overrides import overrides
import pygame

from manager.cfgmgr import Config
from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
import util.colors as color


class MenuValue(TextObject):
    Inst_created: int = 0
    Insts: list[MenuValue] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        MenuValue.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        config = Config().config
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.color = color.white
        self.target_config = self.text
        if config.get(self.target_config) is True:
            self.text = "On"
            pass
        elif config.get(self.target_config) is False:
            self.text = "Off"
            pass
        else:
            self.text = config.get(self.target_config)
            pass
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.midtop = (
            screen_rect.width * 5 // 8,
            screen_rect.height * (2 + self.Inst_created) // 16,
        )
        return None

    @overrides
    def on_destroy(self) -> None:
        MenuValue.Insts.remove(self)
        MenuValue.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in MenuValue.Insts:
            inst.on_destroy()
            del inst
            pass
        MenuValue.Inst_created = 0
        return None

    pass
