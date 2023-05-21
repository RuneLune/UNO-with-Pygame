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
from gameobj.bgobj import BackgroundObject


class StoryBack(GameObject):

    @overrides
    def start(self) -> None:
        
        self.image = pygame.image.load(image_resource(
            join("stage", "map.png")))
        self.rect = self.image.get_rect()
        
        self.z_index = 997

        return None
    
    pass
