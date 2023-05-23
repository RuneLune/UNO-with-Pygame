from overrides import overrides
import pygame

from ..txtbtnobj import TextButtonObject
from .keyinput import KeyInput
import util.colors as color
from util.resource_manager import font_resource


class PasswordButton(TextButtonObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.z_index = 9999
        self.color = color.white
        self.text = "(Set Password)"
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.topright = (
            screen_rect.width * 3 // 4 - screen_rect.height // 32,
            screen_rect.height // 32,
        )
        return None

    @overrides
    def on_click(self) -> None:
        if KeyInput().editing_password:
            KeyInput().editing_password = False
            pass
        else:
            KeyInput().editing_password = True
            pass
        return None

    @overrides
    def update(self) -> None:
        if self.text != KeyInput().current_text:
            if KeyInput().current_text == "":
                self.set_text("(Set Password)")
                pass
            else:
                self.set_text(KeyInput().current_text)
                pass
            pass
        return None

    pass
