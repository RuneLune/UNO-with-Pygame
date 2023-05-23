import pygame
from typing import Tuple

from gameobj.gameobj import GameObject
from util.resource_manager import font_resource
import util.colors as colors

from gameobj.txtobj import TextObject


class WinnerText(TextObject):
    def render(self, text):
        self.text = text
        rendered_text = self.font.render(text, True, self.color)
        return super(TextObject, self).__init__(
            rendered_text,
            self.name,
            self.width,
            self.height,
            self.left,
            self.top,
            self.z_index,
            -1,
        )
