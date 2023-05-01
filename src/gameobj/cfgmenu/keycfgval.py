from __future__ import annotations

import pygame
from overrides import overrides
from typing import List, Type, TYPE_CHECKING, Optional

from ..txtbtnobj import TextButtonObject
from abstrclass.subject import Subject
import util.colors as color
from config.settings_function import Settings

if TYPE_CHECKING:
    from abstrclass.observer import Observer


class KeyConfigValue(TextButtonObject, Subject):
    _selected_color = color.red
    _highlighting_selected_color = color.dark_red

    @overrides
    def start(self) -> None:
        self._observers: List[Type[Observer]] = []
        self._target_key: Optional[str] = None

    @overrides
    def on_click(self) -> None:
        self.notify()
        return None

    def selected(self) -> None:
        self._previous_color, self.color = self.color, self._selected_color
        self._previous_highlighting_color, self.highlighting_color = self.highlighting_color, self._highlighting_selected_color
        if self._mouse_over:
            self.on_mouse_enter()
            pass
        else:
            self.on_mouse_exit()
            pass
        return None

    def unselected(self) -> None:
        self.color = self._previous_color
        self.highlighting_color = self._previous_highlighting_color
        self.text = pygame.key.name(Settings().get_settings().get("key_settings").get(self.target_key))
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

    # @final
    # def target_key(self, value: str) -> KeyConfigValue:
    #     self._target_key = value
    #     return self

    def attach(self, observer: Type[Observer]) -> None:
        self._observers.append(observer)
        return None

    def detach(self, observer: Type[Observer]) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            pass
        return None

    def notify(self) -> None:
        for observer in self._observers:
            observer.observer_update(self)
            continue
        return None

    pass
