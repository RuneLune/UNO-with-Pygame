from __future__ import annotations

from overrides import overrides
import pygame

from gameobj.txtobj import TextObject
from util.resource_manager import font_resource
from metaclass.singleton import SingletonMeta
import util.colors as color
from manager.acvmgr import AchieveManager


class Date(TextObject):
    @overrides
    def start(self) -> None:
        self.achieved = AchieveManager().get_stage_states().get("achieved")
        self.date = AchieveManager().get_stage_states().get("date")
        if self.name == "date_a":
            self.text = self.date[0]
        elif self.name == "date_b":
            self.text = self.date[1]
        elif self.name == "date_c":
            self.text = self.date[2]
        elif self.name == "date_d":
            self.text = self.date[3]
        elif self.name == "date_e":
            self.text = self.date[4]
        elif self.name == "date_f":
            self.text = self.date[5]
        elif self.name == "date_g":
            self.text = self.date[6]
        elif self.name == "date_h":
            self.text = self.date[7]
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self.color = color.white
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self._visible = False
        if self.achieved[0] == True:
            self.visible()
        else: 
            self.invisible()
        self.z_index = 997
        return None

    pass
