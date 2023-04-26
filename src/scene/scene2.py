from .scene import Scene
from overrides import overrides
import pygame

from gameobj.scene2.colorcard import ColorCard
from gameobj.scene2.backbtn import BackButton
from metaclass.singleton import SingletonMeta


class Scene2(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        test_surface1 = pygame.Surface((75, 100))
        test_surface1.fill((255, 255, 255))
        test_surface2 = pygame.Surface((75, 100))
        test_surface2.fill((255, 255, 0))
        test_surface3 = pygame.Surface((75, 100))
        test_surface3.fill((255, 0, 255))
        test_surface4 = pygame.Surface((75, 100))
        test_surface4.fill((0, 255, 255))
        test_surface5 = pygame.Surface((75, 100))
        test_surface5.fill((0, 0, 255))
        test_surface6 = pygame.Surface((75, 100))
        test_surface6.fill((0, 255, 0))
        test_surface7 = pygame.Surface((75, 100))
        test_surface7.fill((255, 0, 0))
        self.instantiate(ColorCard(test_surface1, "Test Object 1", -1, -1, 25, 300, 1))
        self.instantiate(ColorCard(test_surface2, "Test Object 1", -1, -1, 125, 300, 2))
        self.instantiate(ColorCard(test_surface3, "Test Object 1", -1, -1, 225, 300, 3))
        self.instantiate(ColorCard(test_surface4, "Test Object 1", -1, -1, 325, 300, 4))
        self.instantiate(ColorCard(test_surface5, "Test Object 1", -1, -1, 425, 300, 5))
        self.instantiate(ColorCard(test_surface6, "Test Object 1", -1, -1, 525, 300, 6))
        self.instantiate(ColorCard(test_surface7, "Test Object 1", -1, -1, 625, 300, 7))
        back_button = BackButton()
        back_button.attach(self.scene_manager)
        self.instantiate(back_button)
        return None
