from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join


from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
from gameobj.story.storyAtxt import StoryAText
from manager.storymgr import StoryManager
from gameobj.story.handlewindow import HandleWindow
from gameobj.story.yesbtn import YesButton


class IconE(GameObject):
    @overrides
    def start(self) -> None:
        self.image = pygame.image.load(image_resource(
                join("achieve", "a5.png")))
        self.rect = self.image.get_rect()
        self.z_index = 997
        
        return None
    

    

    pass
