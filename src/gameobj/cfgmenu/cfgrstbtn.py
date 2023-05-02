from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING
import pygame

from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
from manager.cfgmgr import Config
import util.colors as color

if TYPE_CHECKING:
    from manager.scenemgr import SceneManager


class ConfigResetButton(TextButtonObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.color = color.white
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.bottomright = (screen_rect.width * 9 // 20, screen_rect.height * 15 // 16)
        return None

    def attach_mgr(self, scene_manager: SceneManager) -> ConfigResetButton:
        self.scene_manager = scene_manager
        return self

    @overrides
    def on_click(self) -> None:
        Config().reset()
        self.scene_manager.reload_scene()
        return None

    pass
