from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING
import pygame

from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta
from manager.lobbymgr import LobbyManager
from manager.soundmgr import SoundManager

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager


class KeyInput(GameObject, metaclass=SingletonMeta):
    _changing_name: bool = False
    previous_name: str = ""

    @overrides
    def on_key_down(self, key: int) -> bool:
        self.key_index = 999
        keyconfig_value = Config().config.get("keybindings")
        if self._changing_name:
            if key == keyconfig_value.get("cancel"):
                LobbyManager().user_name = self.previous_name
                SoundManager().play_effect("click")
                self._changing_name = False
                pass
            elif key == keyconfig_value.get("select"):
                SoundManager().play_effect("click")
                self._changing_name = False
                pass
            elif key == pygame.K_BACKSPACE:
                if len(LobbyManager().user_name) > 1:
                    LobbyManager().user_name = LobbyManager().user_name[:-1]
                    SoundManager().play_effect("click")
                    pass
                pass
            elif key == pygame.K_SPACE:
                if len(LobbyManager().user_name) < 20:
                    LobbyManager().user_name = LobbyManager().user_name + " "
                    SoundManager().play_effect("click")
                    pass
                pass
            elif self.last_event.unicode is not None:
                if len(LobbyManager().user_name) < 20:
                    LobbyManager().user_name = (
                        LobbyManager().user_name + self.last_event.unicode
                    )
                    SoundManager().play_effect("click")
                    pass
                pass
            else:
                return False
            return True
        else:
            if key == keyconfig_value.get("cancel"):
                print("called")
                SoundManager().play_effect("click")
                self.scene_manager.load_previous_scene()
                pass
            elif key == keyconfig_value.get("select"):
                SoundManager().play_effect("click")
                self.changing_name = True
                pass
            pass
        return False

    def attach_mgr(self, scene_manager: SceneManager) -> KeyInput:
        self.scene_manager = scene_manager
        return self

    @property
    def changing_name(self) -> bool:
        return self._changing_name

    @changing_name.setter
    def changing_name(self, value: bool) -> None:
        if value is True:
            self.previous_name = LobbyManager().user_name
            pass
        self._changing_name = value
        return None

    def reset(self) -> None:
        self._changing_name = False
        self.previous_name = ""
        return None

    pass
