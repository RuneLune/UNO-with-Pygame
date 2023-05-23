from __future__ import annotations

from overrides import overrides
import pygame
from os.path import join
import cv2
import numpy

from gameobj.gameobj import GameObject
from gameobj.gamelobby.botAtxt import BotAText
from util.resource_manager import image_resource
from metaclass.singleton import SingletonMeta


class BotAButton(GameObject, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.bot_a_text = BotAText()
        self.image = pygame.image.load(image_resource(join("lobby", "bot_A.png")))
        self.rect = self.image.get_rect()
        self.name = "BotA_Button"
        self.img_copy = self.image
        self.z_index = 2000
        self._visible = False
        self.disable()

        return None

    @overrides
    def on_mouse_enter(self) -> None:
        self.image = self.create_neon(self.image)
        self.bot_a_text.visible()
        self.bot_a_text.enable()
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        self.image = self.img_copy
        self.bot_a_text.invisible()
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
