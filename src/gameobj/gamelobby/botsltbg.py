from __future__ import annotations

from overrides import overrides
import pygame
import util.colors as color

from gameobj.gameobj import GameObject

from metaclass.singleton import SingletonMeta


class BotSelectBackground(GameObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.BotSelect_background_surface = pygame.Surface(screen_rect.size)
        self.BotSelect_background_surface.fill(color.white)
        self.BotSelect_background_surface.set_alpha(200)
        self.image = self.BotSelect_background_surface
        self.name = "BotSelect_background"
        self.z_index = 1999
        self._visible = False

        return None

    pass
