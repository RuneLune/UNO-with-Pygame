from __future__ import annotations

from overrides import overrides
from typing import Type, Dict, TYPE_CHECKING
import pygame

from metaclass.singleton import SingletonMeta
from abstrclass.observer import Observer
from scene.scene import Scene
from scene.scene1 import Scene1
from scene.scene2 import Scene2
from scene.mainmenu import MainMenu

if TYPE_CHECKING:
    from abstrclass.subject import Subject


class SceneManager(Observer, metaclass=SingletonMeta):
    def __init__(self):
        self.scenes: Dict[str, Type[Scene]] = {
            "scene1": Scene1(self),
            "scene2": Scene2(self),
            "main_menu": MainMenu(self),
        }
        self.current_scene = "main_menu"

    @overrides
    def update(self, subject: Type[Subject]) -> None:
        self.current_scene = subject.target_scene
        return None

    def handle_scene(self, event: pygame.event.Event) -> None:
        return self.scenes.get(self.current_scene).handle(event)

    def update_scene(self) -> None:
        return self.scenes.get(self.current_scene).update()

    pass
