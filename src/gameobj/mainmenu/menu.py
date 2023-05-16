from __future__ import annotations

from overrides import overrides
from typing import Optional, TYPE_CHECKING, List
import pygame

from ..txtbtnobj import TextButtonObject
from .keyinput import KeyInput
from util.resource_manager import font_resource
import util.colors as color

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager


class Menu(TextButtonObject):
    Inst_created: int = 0
    Insts: List[Menu] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        Menu.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 13
        )
        self.color = color.black
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.center = (
            screen_rect.centerx,
            screen_rect.height * (6 + self.Inst_created) // 13,
        )
        self._target_scene: Optional[str] = None

    def attach_mgr(
        self, scene_manager: SceneManager, target_scene: Optional[str] = None
    ) -> Menu:
        self.scene_manager = scene_manager
        if target_scene is not None:
            self.target_scene = target_scene
            pass
        return self

    @overrides
    def on_click(self) -> None:
        self.scene_manager.load_scene(self.target_scene)
        return None

    @property
    def target_scene(self) -> str:
        return self._target_scene

    @target_scene.setter
    def target_scene(self, value: str) -> None:
        self._target_scene = value
        return None

    @overrides
    def on_destroy(self) -> None:
        Menu.Insts.remove(self)
        Menu.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in Menu.Insts:
            inst.on_destroy()
            del inst
            pass
        Menu.Inst_created = 0
        return None

    @overrides
    def on_mouse_enter(self) -> None:
        KeyInput().menu_index = Menu.Insts.index(self)
        return super().on_mouse_enter()

    pass
