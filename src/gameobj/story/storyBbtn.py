from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join

from gameobj.story.storyBtxt import StoryBText
from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
import util.colors as color
from manager.storymgr import StoryManager


class StoryBButton(GameObject):
    @overrides
    def start(self) -> None:
        self.story_b_text = StoryBText()
        self.touchable = StoryManager().get_stage_states().get("touchable")
        if self.touchable[1]:
            self.image = pygame.image.load(image_resource(
                join("stage", "story_2.png")))
        else:
            self.image = pygame.image.load(image_resource(
                join("stage", "story_0.png")))
        self.rect = self.image.get_rect()
        self.z_index = 997
        
        return None
    
    
    @overrides
    def on_mouse_enter(self) -> None:
        if self.touchable[1]:
            self.story_b_text.visible()
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        if self.touchable[1]:
            self.story_b_text.invisible()
        return None

    pass
