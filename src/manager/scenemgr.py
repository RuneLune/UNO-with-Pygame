from __future__ import annotations

import pygame
from typing import TYPE_CHECKING

from metaclass.singleton import SingletonMeta
from scene.achieve_scene import AchieveScene
from scene.mainmenu import MainMenu
from scene.cfgmenu import ConfigMenu
from scene.game_scene import GameScene
from scene.story_scene import StoryScene
from scene.gamelobby import GameLobby
from scene.multilobby import MultiLobby
from scene.createserver import CreateServer
from scene.quit import QuitScene

if TYPE_CHECKING:
    from typing import Type, Dict
    from scene.scene import Scene


class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        self.scenes: Dict[str, Type[Scene]] = {
            "achievements": AchieveScene,
            "main_menu": MainMenu,
            "config_menu": ConfigMenu,
            "game_scene": GameScene,
            "story_scene": StoryScene,
            "gamelobby": GameLobby,
            "multilobby": MultiLobby,
            "create_server": CreateServer,
            "quit": QuitScene,
        }
        self.scene_name_list = ["quit", "main_menu"]
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def load_scene(self, scene_name: str) -> None:
        self.scene_name_list.append(scene_name)
        return self._load_scene()

    def _load_scene(self) -> None:
        self.current_scene.exit()
        del self.current_scene
        pygame.display.get_surface().fill((0, 0, 0))
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def reload_scene(self) -> None:
        return self._load_scene()

    def load_previous_scene(self) -> None:
        self.scene_name_list.pop()
        self._load_scene()

    def handle_scene(self, event: pygame.event.Event) -> None:
        return self.current_scene.handle(event)

    def update_scene(self) -> None:
        return self.current_scene.tick()

    @property
    def previous_scene_name(self) -> str:
        if len(self.scene_name_list) >= 2:
            return self.scene_name_list[-2]
        else:
            return "quit"

    @property
    def current_scene_name(self) -> str:
        if self.scene_name_list:
            return self.scene_name_list[-1]
        else:
            return "quit"

    pass
