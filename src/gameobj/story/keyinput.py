from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING, List, Type

from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta



class KeyInput(GameObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self._stage_index = 0
        self._window_index = 0
        self._stage_list = []
        self._window_list = []
        self.window_flag = False
        return None

    @overrides
    def on_key_down(self, key: int) -> bool:
        keyconfig_value = Config().config.get("keybindings")
        if self.window_flag is False:
            if key == keyconfig_value.get("left"):
                self._stage_list[self._stage_index].on_mouse_exit()
                self.stage_index = (self._stage_index - 1) % len(self._stage_list)
                self._stage_list[self._stage_index].on_mouse_enter()
                pass
            elif key == keyconfig_value.get("right"):
                self._stage_list[self._stage_index].on_mouse_exit()
                self.stage_index = (self._stage_index + 1) % len(self._stage_list)
                self._stage_list[self._stage_index].on_mouse_enter()
                pass
            elif key == keyconfig_value.get("select"):
                self._stage_list[self._stage_index].on_mouse_up_as_button()
                pass
            elif key == keyconfig_value.get("cancel"):
                self._back_button.on_click()

        else:
            if key == keyconfig_value.get("left"):
                self._window_list[self._window_index].on_mouse_exit()
                self._window_index = (self._window_index - 1) % len(self._window_list)
                self._window_list[self._window_index].on_mouse_enter()
                pass
            elif key == keyconfig_value.get("right"):
                self._window_list[self._window_index].on_mouse_exit()
                self._window_index = (self._window_index + 1) % len(self._window_list)
                self._window_list[self._window_index].on_mouse_enter()
                pass
            elif key == keyconfig_value.get("select"):
                self._window_list[self._window_index].on_mouse_up_as_button()
                pass
        return False

    def attach_stage(self, stage_list, window_list, back_button) -> None:
        self._stage_list = stage_list
        self._window_list = window_list
        self._back_button = back_button
        return None

    @property
    def stage_index(self) -> int:
        return self._stage_index

    @stage_index.setter
    def stage_index(self, value: int) -> None:
        self._stage_index = value
        return None

    
    def update_flag_true(self):
        self.window_flag = True
        return None
    
    def update_flag_false(self):
        self.window_flag = False
        return None



    pass
