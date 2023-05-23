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


class Locker(GameObject):

    @overrides
    def start(self) -> None:
        self.idx = 0
        for i in range(4):
            if self.name == "b":
                self.idx = 1
            elif self.name == "c":
                self.idx = 2
            elif self.name == "d":
                self.idx = 3
        
        self.touchable = StoryManager().get_stage_states().get("touchable")
        self.image = pygame.image.load(image_resource(
            join("stage", "lock.png")))
        self.rect = self.image.get_rect()
        if self.touchable[self.idx]:
            self.invisible()
        else:
            self.visible()
        self.z_index = 997

        return None

    def set_locker_idx(self, idx):
        self.idx = idx
    pass
