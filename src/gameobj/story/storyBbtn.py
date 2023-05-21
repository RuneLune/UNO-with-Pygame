from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join
import util.colors as color
import cv2
import numpy

from gameobj.story.storyBtxt import StoryBText
from gameobj.gameobj import GameObject
from util.resource_manager import image_resource
from manager.storymgr import StoryManager
from gameobj.story.handlewindow import HandleWindow
from gameobj.story.yesbtn import YesButton
from gameobj.story.keyinput import KeyInput



class StoryBButton(GameObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.story_b_text = StoryBText()
        self.touchable = StoryManager().get_stage_states().get("touchable")
        self.image = pygame.Surface((screen_rect.width / 7 , screen_rect.height / 3),  pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (255, 255, 255, 128), self.rect, 1)
        self.img_copy = self.image
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
    
    @overrides
    def on_mouse_up_as_button(self) -> None:
        if self.touchable[1]:
            KeyInput().update_flag_true()
            HandleWindow().visible_window()
            YesButton().target = "stage_b"
        return super().on_mouse_up_as_button()

    
    pass
