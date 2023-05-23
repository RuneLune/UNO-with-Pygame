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


class Icon(GameObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.achieved = AchieveManager().get_stage_states().get("achieved")
        if int(self.name) == 0:
            image = pygame.image.load(image_resource(
                join("achieve", "a1.png")))
            self.idx = 0
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 1:
            image = pygame.image.load(image_resource(
                join("achieve", "a2.png")))
            self.idx = 1
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 2:
            image = pygame.image.load(image_resource(
                join("achieve", "a3.png")))
            self.idx = 2
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 3:
            image = pygame.image.load(image_resource(
                join("achieve", "a4.png")))
            self.idx = 3
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 4:
            image = pygame.image.load(image_resource(
                join("achieve", "a5.png")))
            self.idx = 4
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 5:
            image = pygame.image.load(image_resource(
                join("achieve", "a6.png")))
            self.idx = 5
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 6:
            image = pygame.image.load(image_resource(
                join("achieve", "a7.png")))
            self.idx = 6
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        elif int(self.name) == 7:
            image = pygame.image.load(image_resource(
                join("achieve", "a8.png")))
            self.idx = 7
            image = pygame.transform.scale(image, size=(screen_rect.height // 8, screen_rect.height // 8))
        
        self.image = image
        
        self.rect = self.image.get_rect()
        self.z_index = 997
        
        return None
    



    pass
