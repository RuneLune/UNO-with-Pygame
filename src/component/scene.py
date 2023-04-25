import pygame
from typing import Type, List

from .gameobj import GameObject


class Scene:
    def __init__(self) -> None:
        self.game_objects: List[Type[GameObject]] = []
        return None

    def create(self, game_object: Type[GameObject]) -> None:
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
