from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join

from gameobj.txtobj import TextObject
from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
import util.colors as color


class YesButton(GameObject):
    @overrides
    def start(self) -> None:
        self.image = pygame.image.load(image_resource(
            join("stage", "yes.png")))
        self.rect = self.image.get_rect()
        self.name = "Yes_Button"
        self.z_index = 999
        self._visible = False
        
        return None
    
    @overrides
    def on_mouse_up_as_button(self) -> None:
        print("yes")
        return None


    pass
