from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING
import pygame
import re
import socket

from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta
from client.client import SocketClient

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager

reg_ip = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
client_ip = socket.gethostbyname(socket.gethostname())


class KeyInput(GameObject, metaclass=SingletonMeta):
    _editing: bool = False
    _current_text: str = client_ip
    _previous_text: str = client_ip

    @overrides
    def on_key_down(self, key: int) -> bool:
        self.key_index = 999
        keyconfig_value = Config().config.get("keybindings")
        if self._editing:
            if key == keyconfig_value.get("cancel"):
                self._current_text = self._previous_text
                # print("stop input")
                pygame.key.stop_text_input()
                self.editing = False
                pass
            elif key == keyconfig_value.get("select"):
                if re.search(reg_ip, self._current_text) is not None:
                    self._previous_text = self._current_text
                    SocketClient().host = self._current_text
                    self.scene_manager.load_scene("multi_lobby")
                    pass
                else:
                    self._current_text = self._previous_text
                    pass
                # print("stop input")
                pygame.key.stop_text_input()
                self.editing = False
                pass
            elif key == pygame.K_BACKSPACE:
                if len(self._current_text) >= 1:
                    self._current_text = self._current_text[:-1]
                    pass
                pass
            # elif self.last_event.unicode is not None:
            #     char = self.last_event.unicode
            #     if ((char >= "0" and char <= "9") or char == ".") and len(
            #         self._current_text
            #     ) < 15:
            #         self._current_text += char
            #         pass
            #     pass
            else:
                return False
            return True
        else:
            if key == keyconfig_value.get("cancel"):
                self.scene_manager.load_previous_scene()
                pass
            elif key == keyconfig_value.get("select"):
                self.editing = True
                # print("start input")
                pygame.key.start_text_input()
                pass
            pass
        return False

    @overrides
    def on_text_input(self, text: str) -> bool:
        if self._editing and len(self._current_text) < 15:
            if (text[-1] >= "0" and text[-1] <= "9") or text[-1] == ".":
                self._current_text += text
                pass
            pass
        # print(text)
        return True

    def attach_mgr(self, scene_manager: SceneManager) -> KeyInput:
        self.scene_manager = scene_manager
        return self

    @property
    def editing(self) -> bool:
        return self._editing

    @editing.setter
    def editing(self, value: bool) -> None:
        # if value is True:
        #     self._previous_text = self._current_text
        #     pass
        self._editing = value
        return None

    @property
    def current_text(self) -> str:
        return self._current_text

    def reset(self) -> None:
        self._current_text = self._previous_text
        self.editing = False
        return None

    pass
