from __future__ import annotations

import pygame
from typing import TYPE_CHECKING

from metaclass.singleton import SingletonMeta
from scene.achieve_scene import AchieveScene
from scene.mainmenu import MainMenu
from scene.selectmenu import SelectMenu
from scene.cfgmenu import ConfigMenu
from scene.game_scene import GameScene
from scene.story_scene import StoryScene
from scene.gamelobby import GameLobby
from scene.multilobby import MultiLobby
from scene.createserver import CreateServer
from scene.joinserver import JoinServer
from scene.quit import QuitScene

if TYPE_CHECKING:
    from typing import Type, Dict
    from scene.scene import Scene


class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        self.scenes: Dict[str, Type[Scene]] = {
            "achievements": AchieveScene,
            "main_menu": MainMenu,
            "select_menu": SelectMenu,
            "config_menu": ConfigMenu,
            "game_scene": GameScene,
            "story_scene": StoryScene,
            "gamelobby": GameLobby,
            "multi_lobby": MultiLobby,
            "create_server": CreateServer,
            "join_server": JoinServer,
            "quit": QuitScene,
        }
        self._back_scene_name = None
        self._scene_name_list = ["quit", "main_menu"]
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def load_scene(self, scene_name: str) -> None:
        self._scene_name_list.append(scene_name)
        return self._load_scene()

    def _load_scene(self) -> None:
        if hasattr(self, "current_scene") and self.current_scene:
            self.current_scene.exit()
            del self.current_scene
        pygame.display.get_surface().fill((0, 0, 0))
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def reload_scene(self) -> None:
        return self._load_scene()

    def load_previous_scene(self) -> None:
        self._back_scene_name = self._scene_name_list.pop()
        self._load_scene()

    def handle_scene(self, event: pygame.event.Event) -> None:
        return self.current_scene.handle(event)

    def update_scene(self) -> None:
        return self.current_scene.tick()

    @property
    def previous_scene_name(self) -> str:
        if len(self._scene_name_list) >= 2:
            return self._scene_name_list[-2]
        else:
            return "quit"

    @property
    def current_scene_name(self) -> str:
        if self._scene_name_list:
            return self._scene_name_list[-1]
        else:
            return "quit"

    @property
    def back_scene_name(self) -> str:
        return self._back_scene_name

    pass
