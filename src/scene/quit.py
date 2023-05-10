from overrides import overrides
import pygame

from .scene import Scene


class QuitScene(Scene):
    @overrides
    def start(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return None

    pass
