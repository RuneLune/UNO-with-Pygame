from __future__ import annotations

import pygame
from overrides import overrides
from typing import Optional

from ..txtbtnobj import TextButtonObject

# from abstrclass.observer import Observer
import util.colors as color
from manager.cfgmgr import Config

# if TYPE_CHECKING:
#     from abstrclass.subject import Subject


class KeyConfigValue(TextButtonObject):
    _selected_color = color.red
    _highlighting_selected_color = color.dark_red

    @overrides
    def start(self) -> None:
        self._target_key: Optional[str] = None
        self._configuring = False

    @overrides
    def on_click(self) -> None:
        self.notify()
        return None

    def keyconfig_start(self) -> None:
        self._previous_color, self.color = self.color, self._selected_color
        self._previous_highlighting_color, self.highlighting_color = (
            self.highlighting_color,
            self._highlighting_selected_color,
        )
        if self._mouse_over:
            self.on_mouse_enter()
            pass
        else:
            self.on_mouse_exit()
            pass
        return None

    def keyconfig_end(self) -> None:
        self.color = self._previous_color
        self.highlighting_color = self._previous_highlighting_color
        self.text = pygame.key.name(
            Config().config.get("key_settings").get(self.target_key)
        )
        if self._mouse_over:
            self.on_mouse_enter()
            pass
        else:
            self.on_mouse_exit()
            pass
        return None

    @property
    def target_key(self) -> str:
        return self._target_key

    @target_key.setter
    def target_key(self, value: str) -> None:
        self._target_key = value
        return None

    # @overrides
    # def observer_update(self, subject: Type[Subject]) -> None:
    #     if self.rect.colliderect(subject.rect):
    #         if not self._configuring:
    #             self._configuring = True
    #             self.selected()
    #             pass
    #         else:
    #             self._configuring = False
    #             self.unselected()
    #             pass
    #         pass
    #     return None

    pass
