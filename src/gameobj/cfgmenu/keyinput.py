from __future__ import annotations

from typing import Type, TYPE_CHECKING
from overrides import overrides

from config.settings_function import Settings
from abstrclass.observer import Observer
from gameobj.gameobj import GameObject

# from metaclass.singleton import SingletonMeta

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class KeyInput(GameObject, Observer):
    _configuring_key = None
    _selected_subject = None

    @overrides
    def on_key_down(self, key: int) -> bool:
        if self._configuring_key is not None:
            if Settings().set_key_value(self._configuring_key, key):
                self._selected_subject.unselected()
                self._selected_subject = None
                self._configuring_key = None
                return True
            pass
        return False

    @overrides
    def observer_update(self, subject: Type[Subject]) -> None:
        if self._configuring_key is None:
            self._configuring_key = subject.target_key
            self._selected_subject = subject
            subject.selected()
            pass
        elif self._configuring_key == subject.target_key:
            self._configuring_key = None
            self._selected_subject = None
            subject.unselected()
            pass
        return None
