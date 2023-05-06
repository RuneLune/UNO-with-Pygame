from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join
from typing import TYPE_CHECKING
import cv2
import numpy

from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
from metaclass.singleton import SingletonMeta

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager

class YesButton(GameObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.image = pygame.image.load(image_resource(
            join("stage", "yes.png")))
        self.rect = self.image.get_rect()
        self.name = "Yes_Button"
        self.img_copy = self.image
        self.z_index = 999
        self._visible = False
        self._target = None
        
        return None
    
    def attach(self, scene_manager: SceneManager) -> None:
        self.scene_manager = scene_manager
        return None
    
    @overrides
    def on_mouse_up_as_button(self) -> None:
    
        self.scene_manager.load_scene(self._target)
        return None
    
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, target):
        self._target = target
        return None
    
    @overrides
    def on_mouse_enter(self) -> None:
        self.image = self.create_neon(self.image)
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        self.image = self.img_copy
        return None

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
