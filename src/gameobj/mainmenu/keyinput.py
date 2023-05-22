from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING, List, Type

from manager.cfgmgr import Config
from manager.soundmgr import SoundManager
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta

if TYPE_CHECKING:
    from .menu import Menu
    from .selector import Selector


class KeyInput(GameObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self._menu_index = 0
        self._menu_list: List[Type[Menu]] = []
        self._selector: Type[Selector] = None
        self.soundManager = SoundManager()
        return None

    @overrides
    def on_key_down(self, key: int) -> bool:
        keyconfig_value = Config().config.get("keybindings")
        if key == keyconfig_value.get("up") or key == keyconfig_value.get("left"):
            self.menu_index = (self._menu_index - 1) % len(self._menu_list)
            pass
        elif key == keyconfig_value.get("down") or key == keyconfig_value.get("right"):
            self.menu_index = (self._menu_index + 1) % len(self._menu_list)
            pass
        elif key == keyconfig_value.get("select"):
            self._menu_list[self._menu_index].on_click()
            self.soundManager.stop_main_background_sound()
            pass
        self.soundManager.play_effect("click")
        return False

    def attach_menu(self, menu_list: List[Type[Menu]]) -> None:
        self._menu_list = menu_list
        return None

    def attach_selector(self, selector: Type[Selector]) -> KeyInput:
        self._selector = selector
        return self

    @property
    def menu_index(self) -> int:
        return self._menu_index

    @menu_index.setter
    def menu_index(self, value: int) -> None:
        self._menu_index = value
        self.on_index_change()
        return None

    def on_index_change(self) -> None:
        if self._selector is not None:
            self._selector.center = self._menu_list[self._menu_index].center
        return None

    @overrides
    def update(self) -> None:
        if self._selector is not None and self._menu_list:
            self._selector.center = self._menu_list[self._menu_index].center
            pass
        return None

    pass
