from __future__ import annotations

import pygame
from typing import TYPE_CHECKING

from metaclass.singleton import SingletonMeta
from scene.test import TestScene
from scene.mainmenu import MainMenu
from scene.cfgmenu import ConfigMenu
from scene.game_scene import GameScene
from scene.story_scene import StoryScene
from scene.gamelobby import GameLobby
from scene.quit import QuitScene

if TYPE_CHECKING:
    from typing import Type, Dict
    from scene.scene import Scene


class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        self.scenes: Dict[str, Type[Scene]] = {
            "test": TestScene,
            "main_menu": MainMenu,
            "config_menu": ConfigMenu,
            "game_scene": GameScene,
            "story_scene": StoryScene,
            "gamelobby": GameLobby,
            "quit": QuitScene,
        }
        self.current_scene_name = "main_menu"
        self.current_scene = self.scenes[self.current_scene_name](self)
        self.previous_scene = None

    def load_scene(self, scene_name: str) -> None:
        self.previous_scene_name = self.current_scene_name
        self.current_scene_name = scene_name
        self.current_scene.exit()
        del self.current_scene
        pygame.display.get_surface().fill((0, 0, 0))
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def reload_scene(self) -> None:
        self.current_scene.exit()
        del self.current_scene
        pygame.display.get_surface().fill((0, 0, 0))
        self.current_scene = self.scenes[self.current_scene_name](self)
        return None

    def load_previous_scene(self) -> None:
        return self.load_scene(self.previous_scene_name)

    def handle_scene(self, event: pygame.event.Event) -> None:
        return self.current_scene.handle(event)

    def update_scene(self) -> None:
        return self.current_scene.tick()

    pass
