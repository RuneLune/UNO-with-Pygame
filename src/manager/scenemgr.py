from __future__ import annotations

from typing import Type, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import pygame

from metaclass.singleton import SingletonMeta
from scene.scene import Scene
from scene.scene1 import Scene1
from scene.scene2 import Scene2
from scene.mainmenu import MainMenu
from scene.cfgmenu import ConfigMenu


class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        self.scenes: Dict[str, Type[Scene]] = {
            "scene1": Scene1,
            "scene2": Scene2,
            "main_menu": MainMenu,
            "config_menu": ConfigMenu,
        }
        self.current_scene_name = "main_menu"
        self.current_scene = self.scenes[self.current_scene_name](self)
        self.previous_scene = None

    def load_scene(self, scene_name: str) -> None:
        self.previous_scene_name = self.current_scene_name
        self.current_scene_name = scene_name
        self.current_scene.exit()
        del self.current_scene
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def reload_scene(self) -> None:
        self.current_scene.exit()
        del self.current_scene
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def load_previous_scene(self) -> None:
        return self.load_scene(self.previous_scene_name)

    def handle_scene(self, event: pygame.event.Event) -> None:
        return self.current_scene.handle(event)

    def update_scene(self) -> None:
        return self.current_scene.tick()

    pass
