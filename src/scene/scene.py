from __future__ import annotations

import pygame
from typing import Type, List, TYPE_CHECKING

from gameobj.gameobj import GameObject

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager


class Scene:
    def __init__(self, scene_manager: SceneManager) -> None:
        self.scene_manager: SceneManager = scene_manager
        self.game_objects: List[Type[GameObject]] = []
        self.start()
        return None

    def start(self) -> None:
        """Scene에 필요한 GameObject 추가"""
        return None

    def instantiate(self, game_object: Type[GameObject]) -> None:
        self.game_objects.append(game_object)
        return None

    def destroy(self, game_object: Type[GameObject]) -> None:
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)
            game_object.on_destroy()
            pass
        else:
            raise ValueError("game_object not found")
        return None

    def update(self) -> None:
        self.game_objects.sort()
        if self.game_objects:
            for game_object in self.game_objects:
                game_object.tick()
                continue
            pass
        return None

    def handle(self, event: Type[pygame.event.Event]) -> None:
        if self.game_objects:
            for game_object in reversed(self.game_objects):
                if game_object.handle(event):
                    break
                continue
            pass
        return None

    pass
