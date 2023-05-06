from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join

from gameobj.txtobj import TextObject
from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
import util.colors as color


class WindowBackground(GameObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.window_background_surface = pygame.Surface(screen_rect.size)
        self.window_background_surface.fill((255, 255, 255))
        self.window_background_surface.set_alpha(200)
        self.image = self.window_background_surface
        self.name = "window_background"
        self.z_index = 998
        self._visible = False
        
        return None

    pass
