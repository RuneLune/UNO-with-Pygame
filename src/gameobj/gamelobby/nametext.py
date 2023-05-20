from overrides import overrides
import pygame

from ..txtobj import TextObject
from .keyinput import KeyInput
from manager.lobbymgr import LobbyManager
from util.resource_manager import font_resource
import util.colors as color


class NameText(TextObject):
    @overrides
    def start(self) -> None:
        self.z_index = 1000
        self.key_index = -1000
        screen_rect = pygame.display.get_surface().get_rect()
        self.text = LobbyManager().user_name
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 15
        )
        self.image = self.font.render(self.text, True, color.white)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_rect.width * 3 // 8, screen_rect.height // 3)
        return None

    @overrides
    def on_key_down(self, key: int) -> bool:
        self.text = LobbyManager().user_name
        self.image = self.font.render(self.text, True, color.white)
        coordinate = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = coordinate
        if KeyInput().changing_name:
            pygame.draw.rect(self.image, color.white, pygame.Rect((0, 0), self.rect.size), 2)
            pass
        return False
