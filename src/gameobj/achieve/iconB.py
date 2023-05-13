from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join
import cv2
import numpy


from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
from util.resource_manager import image_resource
from manager.acvmgr import AchieveManager


class IconB(GameObject):
    @overrides
    def start(self) -> None:
        self.achieved = AchieveManager().get_stage_states().get("achieved")
        image = pygame.image.load(image_resource(
                join("achieve", "a2.png")))
        image2 = self.create_neon(image)
        if self.achieved[1] == True:
            self.image = image
        else:
            self.image = image2
        self.rect = self.image.get_rect()
        self.z_index = 997
        
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
