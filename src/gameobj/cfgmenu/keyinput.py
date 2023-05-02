# from __future__ import annotations

from overrides import overrides

from manager.cfgmgr import Config
from gameobj.gameobj import GameObject


class KeyInput(GameObject):
    _configuring_key = None
    _selecting_menu = None

    @overrides
    def start(self) -> None:
        self._menu_index = 0
        self._menu_list = []
        self._left_button_list = []
        self._right_button_list = []
        self._key_button_list = []
        return None

    @overrides
    def on_key_down(self, key: int) -> bool:
        keyconfig_value = Config().config.get("keybindings")
        if self._configuring_key is not None:
            if Config().set_key_value(self._configuring_key, key):
                self._configuring_key = None
                self.notify()
                return True
            pass
        elif key == keyconfig_value.get("up"):
            pass
        elif key == keyconfig_value.get("down"):
            pass
        elif key == keyconfig_value.get("left"):
            pass
        elif key == keyconfig_value.get("right"):
            pass
        elif key == keyconfig_value.get("select"):
            pass
        elif key == keyconfig_value.get("cancel"):
            pass

        return False

    def attach_menu(self, menu) -> None:
        self._menu_list.append(menu)
        return None

    def attach_left_button(self, button, index) -> None:
        self._left_button_list[index] = button
        return None

    def attach_right_button(self, button, index) -> None:
        self._right_button_list[index] = button
        return None

    def attach_key_button(self, button, index) -> None:
        self._key_button_list[index] = button
        return None

    pass
