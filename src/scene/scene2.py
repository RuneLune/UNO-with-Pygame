from .scene import Scene
from overrides import overrides
import pygame

from gameobj.scene2.bg import Background
from gameobj.scene2.colorcard import ColorCard
from gameobj.scene2.backbtn import BackButton
from metaclass.singleton import SingletonMeta


class Scene2(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.background = Background()
        self.back_button = BackButton()
        self.test_surface1 = pygame.Surface((75, 100))
        self.test_surface2 = pygame.Surface((75, 100))
        self.test_surface3 = pygame.Surface((75, 100))
        self.test_surface4 = pygame.Surface((75, 100))
        self.test_surface5 = pygame.Surface((75, 100))
        self.test_surface6 = pygame.Surface((75, 100))
        self.test_surface7 = pygame.Surface((75, 100))

        self.test_surface1.fill((255, 255, 255))
        self.test_surface2.fill((255, 255, 0))
        self.test_surface3.fill((255, 0, 255))
        self.test_surface4.fill((0, 255, 255))
        self.test_surface5.fill((0, 0, 255))
        self.test_surface6.fill((0, 255, 0))
        self.test_surface7.fill((255, 0, 0))

        self.back_button.on_mouse_up_as_button = (
            lambda: self.scene_manager.load_previous_scene()
        )

        self.instantiate(self.background)
        self.instantiate(self.back_button)
        self.instantiate(
            ColorCard(self.test_surface1, "Test Object 1", -1, -1, 25, 300, 1)
        )
        self.instantiate(
            ColorCard(self.test_surface2, "Test Object 1", -1, -1, 125, 300, 2)
        )
        self.instantiate(
            ColorCard(self.test_surface3, "Test Object 1", -1, -1, 225, 300, 3)
        )
        self.instantiate(
            ColorCard(self.test_surface4, "Test Object 1", -1, -1, 325, 300, 4)
        )
        self.instantiate(
            ColorCard(self.test_surface5, "Test Object 1", -1, -1, 425, 300, 5)
        )
        self.instantiate(
            ColorCard(self.test_surface6, "Test Object 1", -1, -1, 525, 300, 6)
        )
        self.instantiate(
            ColorCard(self.test_surface7, "Test Object 1", -1, -1, 625, 300, 7)
        )
        return None
