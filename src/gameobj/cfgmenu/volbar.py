from __future__ import annotations

from overrides import overrides
import pygame

from manager.cfgmgr import Config
from manager.soundmgr import SoundManager
from ..barobj import BarObject
import util.colors as color
from util.resource_manager import font_resource


class VolumeBar(BarObject):
    Inst_created: int = 0
    Insts: list[VolumeBar] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        VolumeBar.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self._background_color = color.dark_gray
        self._cover_color = color.white
        self._min_value = 0
        self._max_value = 100
        self._value = 50
        self._vertical = True
        self._width = screen_rect.width // 22
        self._height = screen_rect.height // 2
        self.image = pygame.Surface((self._width, self._height))
        self.rect = self.image.get_rect()
        self.rect.center = (
            screen_rect.width * (13 + self.Inst_created) // 17,
            screen_rect.height // 2,
        )
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 32
        )
        self._draw_bar()
        self.draw_value()
        return None

    def set_target(self, target_volume: str) -> VolumeBar:
        self._target_volume = target_volume
        self._value = Config().get_volume(target_volume)
        self._draw_bar()
        self.draw_value()
        return self

    @overrides
    def on_bar_move(self) -> None:
        Config().set_volume(self._target_volume, self._value)
        SoundManager().update_all_volume()
        self.draw_value()
        return None

    def draw_value(self) -> None:
        value_text = self.font.render(str(self._value), True, color.black)
        value_text_rect = value_text.get_rect()
        value_text_rect.midbottom = (self.rect.width // 2, self.rect.height)
        self.image.blit(value_text, value_text_rect)
        return None

    @overrides
    def on_destroy(self) -> None:
        VolumeBar.Insts.remove(self)
        VolumeBar.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in VolumeBar.Insts:
            inst.on_destroy()
            del inst
            pass
        VolumeBar.Inst_created = 0
        return None

    pass
