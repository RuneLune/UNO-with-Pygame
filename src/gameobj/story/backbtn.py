from __future__ import annotations

from overrides import overrides
from typing import Tuple
from typing import TYPE_CHECKING
import pygame

from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
import util.colors as color
from manager.soundmgr import SoundManager


if TYPE_CHECKING:
    from manager.scenemgr import SceneManager
    


class BackButton(TextButtonObject):
    @overrides
    def start(self) -> None:
        self.highlighting_color = color.black
        self.soundmanager = SoundManager()
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.color = color.white
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.bottomleft = (screen_rect.width * 11 // 40, screen_rect.height * 15 // 16)
        return None

    def attach_mgr(self, scene_manager: SceneManager) -> BackButton:
        self.scene_manager = scene_manager
        return self

    @overrides
    def on_click(self) -> None:
        self.scene_manager.load_previous_scene()
        self.soundmanager.play_effect("click")
        return None
    
    def change_highlighting_color(self, color: Tuple[int, int, int]) -> None:
        self.highlighting_color = color
        return None

    pass
