from overrides import overrides
import pygame

from ..txtbtnobj import TextButtonObject
from .keyinput import KeyInput
import util.colors as color
from util.resource_manager import font_resource


class PasswordText(TextButtonObject):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        self.z_index = 9999
        self.color = color.black
        self.text = "(Password)"
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 15
        )
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.midtop = screen_rect.center
        return None

    # @overrides
    # def on_click(self) -> None:
    #     if KeyInput().editing_password:
    #         KeyInput().editing_password = False
    #         pass
    #     else:
    #         KeyInput().editing_password = True
    #         pass
    #     return None

    @overrides
    def update(self) -> None:
        if self.text != KeyInput().current_pwd_text:
            if KeyInput().current_pwd_text == "":
                self.set_text("(Password)")
                pass
            else:
                self.set_text(KeyInput().current_pwd_text)
                pass
            pass
        return None

    pass
