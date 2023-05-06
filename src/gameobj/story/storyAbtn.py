from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join
import cv2
import numpy

from gameobj.txtobj import TextObject
from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
from gameobj.story.storyAtxt import StoryAText
import util.colors as color
from manager.storymgr import StoryManager
from gameobj.story.handlewindow import HandleWindow
from gameobj.story.yesbtn import YesButton


class StoryAButton(GameObject):
    @overrides
    def start(self) -> None:
        self.story_a_text = StoryAText()
        self.touchable = StoryManager().get_stage_states().get("touchable")
        if self.touchable[0]:
            self.image = pygame.image.load(image_resource(
                join("stage", "story_1.png")))
        else:
            self.image = pygame.image.load(image_resource(
                join("stage", "story_0.png")))
        self.rect = self.image.get_rect()
        self.img_copy = self.image
        self.z_index = 997
        
        return None
    
    @overrides
    def on_mouse_enter(self) -> None:
        if self.touchable[0]:
            self.image = self.create_neon(self.image)
            self.story_a_text.visible()
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        if self.touchable[0]:
            self.image = self.img_copy
            self.story_a_text.invisible()
        return None
    
    @overrides
    def on_mouse_up_as_button(self) -> None:
        if self.touchable[0]:
            HandleWindow().visible_window()
            YesButton().target = "storyA"
        return super().on_mouse_up_as_button()


    def create_neon(self, surf):
        surf_alpha = surf.convert_alpha()
        rgb = pygame.surfarray.array3d(surf_alpha)
        alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
        image = numpy.concatenate((rgb, alpha), 2)
        cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
        cv2.blur(image, ksize=(5, 5), dst=image)
        bloom_surf = pygame.image.frombuffer(
            image.flatten(), image.shape[1::-1], "RGBA"
        )
        bloom_surf = pygame.transform.rotate(bloom_surf, 270)
        bloom_surf = pygame.transform.flip(bloom_surf, True, False)
        return bloom_surf

    pass
