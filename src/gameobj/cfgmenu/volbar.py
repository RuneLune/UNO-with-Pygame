from __future__ import annotations

from overrides import overrides
import pygame

from manager.cfgmgr import Config
from manager.soundmgr import SoundManager
from ..barobj import BarObject
import util.colors as color


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
        self._background_color = color.white
        self._cover_color = color.green
        self._min_value = 0
        self._max_value = 100
        self._value = 50
        self._vertical = True
        self._width = screen_rect.width // 20
        self._height = screen_rect.height // 2
        self.rect = pygame.Rect((0, 0), (self._width, self._height))
        self.center = (
            screen_rect.width * (16 + self.Inst_created) // 20,
            screen_rect.height // 2,
        )
        return None

    def set_target(self, target_volume: str) -> VolumeBar:
        self._target_volume = target_volume
        self._value = Config().get_volume(target_volume)
        return self

    @overrides
    def on_bar_move(self) -> None:
        Config().set_volume(self._target_volume, self._value)
        SoundManager().update_all_volume()
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
