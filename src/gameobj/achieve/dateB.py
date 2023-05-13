from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
from metaclass.singleton import SingletonMeta
import util.colors as color
from manager.acvmgr import AchieveManager


class DateB(TextObject):
    @overrides
    def start(self) -> None:
        self.achieved = AchieveManager().get_stage_states().get("achieved")
        self.date = AchieveManager().get_stage_states().get("date")
        self.text = self.date[1]
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self.color = color.white
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        if self.achieved[1] == True:
            self.visible()
        else: 
            self.invisible()
        self.z_index = 997
        return None

    pass
