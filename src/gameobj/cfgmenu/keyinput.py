from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING

from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta
from .keymenuval import KeyMenuValue

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager


class KeyInput(GameObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self._menu_index = 0
        self._menu_list = []
        self._left_button_list = []
        self._right_button_list = []
        self._key_button_list = []
        self._configuring_key = None
        return None

    def attach_mgr(self, scene_manager: SceneManager) -> KeyInput:
        self.scene_manager = scene_manager
        return self

    @overrides
    def on_key_down(self, key: int) -> bool:
        keyconfig_value = Config().config.get("keybindings")
        if self._configuring_key is not None:
            if Config().set_key_value(self._configuring_key, key):
                for inst in KeyMenuValue.Insts:
                    if inst.target_config_key == self._configuring_key:
                        inst.keybind_end()
                        break
                    continue
                self._configuring_key = None
                self.scene_manager.reload_scene()
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

    @property
    def configuring_key(self) -> str:
        return self._configuring_key

    @configuring_key.setter
    def configuring_key(self, key: str) -> None:
        if self._configuring_key is not None:
            for inst in KeyMenuValue.Insts:
                if inst.target_config_key == self._configuring_key:
                    inst.keybind_end()
                    break
                continue
            pass
        if self._configuring_key == key:
            self._configuring_key = None
            pass
        else:
            self._configuring_key = key
            for inst in KeyMenuValue.Insts:
                if inst.target_config_key == self._configuring_key:
                    inst.keybind_start()
                    break
                continue
            pass
        return None

    pass
