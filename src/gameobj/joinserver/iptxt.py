from overrides import overrides
import pygame

from ..txtobj import TextObject
from .keyinput import KeyInput
from util.resource_manager import font_resource
import util.colors as color


class IPText(TextObject):
    @overrides
    def start(self) -> None:
        self.color = color.black
        self.z_index = 1000
        self.key_index = -1000
        screen_rect = pygame.display.get_surface().get_rect()
        self.text = KeyInput().current_ip_text
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 15
        )
        self.image = self.font.render(self.text, True, self.color)
        self.size = self.image.get_rect().size
        self.midbottom = screen_rect.center
        return None

    @overrides
    def update(self) -> None:
        if self.text != KeyInput().current_ip_text:
            self.set_text(KeyInput().current_ip_text)
            pass
        return None

    pass
