from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join
import cv2
import numpy

from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
from gameobj.story.storyAtxt import StoryAText
from manager.storymgr import StoryManager
from gameobj.story.handlewindow import HandleWindow
from gameobj.story.yesbtn import YesButton
from gameobj.story.keyinput import KeyInput


class Cat(GameObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.story_a_text = StoryAText()
        self.touchable = StoryManager().get_stage_states().get("touchable")
        image = pygame.image.load(image_resource(
            join("stage", "cat.png")))
        self.image = pygame.transform.scale(image, size=(screen_rect.width, screen_rect.height))
        self.rect = self.image.get_rect()
        
        self.z_index = -999
        
        return None
    
    