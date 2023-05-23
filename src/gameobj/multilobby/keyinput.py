from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING
import pygame

from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta
from client.client import SocketClient

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager


class KeyInput(GameObject, metaclass=SingletonMeta):
    _editing_password: bool = False
    _current_text: str = ""
    _previous_text: str = ""

    @overrides
    def on_key_down(self, key: int) -> bool:
        self.key_index = 999
        keyconfig_value = Config().config.get("keybindings")
        if self._editing_password:
            if key == keyconfig_value.get("cancel"):
                self._current_text = self._previous_text
                pygame.key.stop_text_input()
                self.editing_password = False
                pass
            elif key == keyconfig_value.get("select"):
                self._previous_text = self._current_text
                pygame.key.stop_text_input()
                self.editing_password = False
                pass
            elif key == pygame.K_BACKSPACE:
                if len(self._current_text) >= 1:
                    self._current_text = self._current_text[:-1]
                    pass
                pass
            else:
                return False
            return True
        else:
            if key == keyconfig_value.get("cancel"):
                self.scene_manager.load_previous_scene()
                pass
            elif key == keyconfig_value.get("select"):
                self.editing_password = True
                pygame.key.start_text_input()
                pass
            pass
        return False

    @overrides
    def on_text_input(self, text: str) -> bool:
        if self._editing_password and len(self._current_text) < 15:
            self._current_text += text
            pass
        return True

    def attach_mgr(self, scene_manager: SceneManager) -> KeyInput:
        self.scene_manager = scene_manager
        return self

    @property
    def editing_password(self) -> bool:
        return self._editing_password

    @editing_password.setter
    def editing_password(self, value: bool) -> None:
        if value is True:
            self._previous_text = self._current_text
            pass
        else:
            SocketClient().send_data("OWNER", "SETPASS", self._current_text)
        self._editing_password = value
        return None

    @property
    def current_text(self) -> str:
        return self._current_text

    def reset(self) -> None:
        self._current_text = self._previous_text
        self._editing_password = False
        return None

    pass
