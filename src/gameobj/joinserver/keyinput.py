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
    _editing_ip: bool = False
    _editing_password: bool = False
    _current_ip_text: str = client_ip
    _previous_ip_text: str = client_ip
    _current_pwd_text: str = ""
    _previous_pwd_text: str = ""

    @overrides
    def on_key_down(self, key: int) -> bool:
        self.key_index = 999
        keyconfig_value = Config().config.get("keybindings")
        if self._editing_ip:
            if key == keyconfig_value.get("cancel"):
                self._current_ip_text = self._previous_ip_text
                pygame.key.stop_text_input()
                self.editing_ip = False
                pass
            elif key == keyconfig_value.get("select"):
                if re.search(reg_ip, self._current_ip_text) is not None:
                    self._previous_ip_text = self._current_ip_text
                    SocketClient().host = self._current_ip_text
                    # self.scene_manager.load_scene("multi_lobby")
                    pass
                else:
                    self._current_ip_text = self._previous_ip_text
                    pass
                # pygame.key.stop_text_input()
                self.editing_ip = False
                self.editing_password = True
                # pygame.key.start_text_input()
                pass
            elif key == pygame.K_BACKSPACE:
                if len(self._current_ip_text) >= 1:
                    self._current_ip_text = self._current_ip_text[:-1]
                    pass
                pass
            else:
                return False
            return True
        elif self.editing_password:
            if key == keyconfig_value.get("cancel"):
                self._current_pwd_text = self._previous_pwd_text
                pygame.key.stop_text_input()
                self.editing_password = False
                pass
            elif key == keyconfig_value.get("select"):
                self._previous_pwd_text = self._current_pwd_text
                pygame.key.stop_text_input()
                SocketClient().password = self._current_pwd_text
                self.editing_password = False
                self.scene_manager.load_scene("multi_lobby")
                pass
            elif key == pygame.K_BACKSPACE:
                if len(self._current_pwd_text) >= 1:
                    self._current_pwd_text = self._current_pwd_text[:-1]
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
                self.editing_ip = True
                pygame.key.start_text_input()
                pass
            pass
        return False

    @overrides
    def on_text_input(self, text: str) -> bool:
        if self._editing_ip and len(self._current_ip_text) < 15:
            if (text[-1] >= "0" and text[-1] <= "9") or text[-1] == ".":
                self._current_ip_text += text
                pass
            pass
        elif self._editing_password and len(self._current_pwd_text) < 8:
            self._current_pwd_text += text
            pass
        return True

    def attach_mgr(self, scene_manager: SceneManager) -> KeyInput:
        self.scene_manager = scene_manager
        return self

    @property
    def editing_ip(self) -> bool:
        return self._editing_ip

    @editing_ip.setter
    def editing_ip(self, value: bool) -> None:
        # if value is True:
        #     self._previous_ip_text = self._current_ip_text
        #     pass
        self._editing_ip = value
        return None

    @property
    def current_ip_text(self) -> str:
        return self._current_ip_text

    @property
    def current_pwd_text(self) -> str:
        return self._current_pwd_text

    @property
    def editing_password(self) -> bool:
        return self._editing_password

    @editing_password.setter
    def editing_password(self, value: bool) -> None:
        self._editing_password = value
        return None

    def reset(self) -> None:
        self._current_ip_text = self._previous_ip_text
        self.editing_ip = False
        return None

    pass
