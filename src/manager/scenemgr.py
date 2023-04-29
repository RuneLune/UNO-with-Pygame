from typing import Type, Dict
import pygame

from metaclass.singleton import SingletonMeta
from scene.scene import Scene
from scene.scene1 import Scene1
from scene.scene2 import Scene2
from scene.mainmenu import MainMenu


class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        self.scenes: Dict[str, Type[Scene]] = {
            "scene1": Scene1(self),
            "scene2": Scene2(self),
            "main_menu": MainMenu(self),
        }
        self.current_scene = "main_menu"
        self.previous_scene = "main_menu"

    def load_scene(self, scene_name: str) -> None:
        self.previous_scene = self.current_scene
        self.current_scene = scene_name
        return None

    def load_previous_scene(self) -> None:
        return self.load_scene(self.previous_scene)

    def handle_scene(self, event: pygame.event.Event) -> None:
        return self.scenes.get(self.current_scene).handle(event)

    def update_scene(self) -> None:
        return self.scenes.get(self.current_scene).tick()

    pass
