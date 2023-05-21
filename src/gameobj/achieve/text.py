from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
from metaclass.singleton import SingletonMeta
import util.colors as color
from manager.acvmgr import AchieveManager

class Text(TextObject):
    @overrides
    def start(self) -> None:
        self.achieved = AchieveManager().get_stage_states().get("achieved")
        if self.name == "0":
            self.text = AchieveManager().get_achieve_text(0)
        if self.name == "1":
            self.text = AchieveManager().get_achieve_text(1)
        if self.name == "2":
            self.text = AchieveManager().get_achieve_text(2)
        if self.name == "3":
            self.text = AchieveManager().get_achieve_text(3)
        if self.name == "4":
            self.text = AchieveManager().get_achieve_text(4)
        if self.name == "5":
            self.text = AchieveManager().get_achieve_text(5)
        if self.name == "6":
            self.text = AchieveManager().get_achieve_text(6)
        if self.name == "7":
            self.text = AchieveManager().get_achieve_text(7)
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        if self.achieved[0] == True:
            self.color = color.white
        else: 
            self.color = color.gray
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.z_index = 997
        return None

    pass
