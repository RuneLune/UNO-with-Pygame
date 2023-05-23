from overrides import overrides
import pygame

from .scene import Scene


class QuitScene(Scene):
    @overrides
    def update(self) -> None:
        if not hasattr(self, "update_called"):
            self.update_called = True
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            pass
        return None

    pass
