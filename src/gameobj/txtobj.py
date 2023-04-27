import pygame
from typing import Tuple

from .gameobj import GameObject
from util.resource_manager import font_resource
import util.colors as colors

pygame.init()


class TextObject(GameObject):
    def __init__(
        self,
        text: str = "TextObject",
        font: pygame.font.Font = pygame.font.Font(font_resource("MainFont.ttf"), 10),
        color: Tuple[int, int, int] = colors.black,
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
    ) -> None:
        self.text = text
        self.font = font
        self.color = color
        rendered_text = font.render(text, True, color)
        return super(TextObject, self).__init__(
            rendered_text, name, width, height, left, top, z_index
        )
