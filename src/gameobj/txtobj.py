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
        screen: pygame.Surface = None,
    ) -> None:
        self.text = text
        self.font = font
        self.color = color
        rendered_text = font.render(text, True, color)
        return super(TextObject, self).__init__(
            rendered_text, name, width, height, left, top, z_index, -1, screen
        )

    def set_text(self, text: str) -> None:
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        rect = pygame.Rect(self.image.get_rect())
        if self._last_x_position == "center":
            rect.centerx = self.rect.centerx
            pass
        elif self._last_x_position == "right":
            rect.right = self.rect.right
            pass
        elif self._last_x_position == "left":
            rect.left = self.rect.left
            pass
        else:
            pass
        if self._last_y_position == "center":
            rect.centery = self.rect.centery
            pass
        elif self._last_y_position == "bottom":
            rect.bottom = self.rect.bottom
            pass
        elif self._last_y_position == "top":
            rect.top = self.rect.top
            pass
        else:
            pass
        self.rect = rect
        return None

    pass
