from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING
import pygame

from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
import util.colors as color
from manager.soundmgr import SoundManager
from client.client import SocketClient

if TYPE_CHECKING:
    from gameobj.multilobby.playerarea import PlayerArea
    from gameobj.multilobby.userarea import UserArea


class KickButton(TextButtonObject):
    Inst_created: int = 0
    Insts: list[KickButton] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        self.soundmanager = SoundManager()
        self.socket_client = SocketClient()
        KickButton.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self.idx = KickButton.Inst_created - 1
        self.color = color.red
        self.text = "KICK"
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.topright = (
            screen_rect.width - screen_rect.height // 100,
            screen_rect.height // 5 * (KickButton.Inst_created - 1)
            + screen_rect.height // 100,
        )
        self.z_index = 9999
        self.invisible()
        return None

    def attach_player_area(self, player_area: PlayerArea) -> KickButton:
        self.player_area = player_area
        return self

    def attach_user_area(self, user_area: UserArea) -> KickButton:
        self.user_area = user_area
        return self

    @overrides
    def on_click(self) -> None:
        self.soundmanager.play_effect("click")
        if self.player_area.nametxt != "":
            self.socket_client.send_data("OWNER", "KICK", self.player_area.nametxt)
            pass
        return None

    @overrides
    def on_destroy(self) -> None:
        KickButton.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in KickButton.Insts:
            inst.on_destroy()
            del inst
            pass
        KickButton.Inst_created = 0
        return None

    @overrides
    def update(self) -> None:
        if self.player_area.nametxt == "":
            self.invisible()
            pass
        elif self.user_area.is_owner:
            self.visible()
            pass
        return None

    # @overrides
    # def on_became_invisible(self) -> None:
    #     print(f"{self.idx}: invisible")
    #     return None

    # @overrides
    # def on_became_visible(self) -> None:
    #     print(f"{self.idx}: visible")
    #     return None

    pass
