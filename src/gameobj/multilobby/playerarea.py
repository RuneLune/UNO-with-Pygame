from __future__ import annotations

from typing import List, Tuple
from overrides import overrides
import pygame

from gameobj.gameobj import GameObject
import util.colors as color
from util.resource_manager import font_resource


class PlayerArea(GameObject):
    Inst_created = 0
    Insts: List[PlayerArea] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        PlayerArea.Insts.append(self)
        self.idx = PlayerArea.Inst_created - 1
        screen_rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface((screen_rect.width // 4, screen_rect.height // 5))
        self._bg_color = color.dark_slate_gray
        self._bd_color = color.white
        self._txt_color = color.white
        self._nametxt = ""
        self._font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 30
        )
        self._is_owner = False
        self._draw_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            screen_rect.width * 3 // 4,
            screen_rect.height // 5 * (PlayerArea.Inst_created - 1),
        )
        self.z_index = 100

        return None

    def _draw_image(self) -> None:
        image_rect = self.image.get_rect()
        self.image.fill(self._bg_color)
        pygame.draw.rect(
            self.image,
            self._bd_color,
            image_rect,
            2,
        )
        # render and draw text
        if self.is_owner:
            text = self._font.render("☆" + self._nametxt, True, self._txt_color)
            pass
        else:
            text = self._font.render(self._nametxt, True, self._txt_color)
            pass
        text_rect = text.get_rect()
        text_rect.topleft = (image_rect.height // 20, image_rect.height // 20)
        self.image.blit(text, text_rect)
        return None

    @overrides
    def on_destroy(self) -> None:
        PlayerArea.Insts.remove(self)
        PlayerArea.Inst_created -= 1
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in PlayerArea.Insts:
            inst.on_destroy()
            del inst
            pass
        PlayerArea.Inst_created = 0
        return None

    @property
    def bg_color(self) -> Tuple[int, int, int]:
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value: Tuple[int, int, int]) -> None:
        self._bg_color = value
        self._draw_image()
        return None

    @property
    def bd_color(self) -> Tuple[int, int, int]:
        return self._bd_color

    @bd_color.setter
    def bd_color(self, value: Tuple[int, int, int]) -> None:
        self._bd_color = value
        self._draw_image()
        return None

    @property
    def txt_color(self) -> Tuple[int, int, int]:
        return self._txt_color

    @txt_color.setter
    def txt_color(self, value: Tuple[int, int, int]) -> None:
        self._txt_color = value
        self._draw_image()
        return None

    @property
    def nametxt(self) -> str:
        return self._nametxt

    @nametxt.setter
    def nametxt(self, value: str) -> None:
        self._nametxt = value
        self._draw_image()
        return None

    @property
    def is_owner(self) -> bool:
        return self._is_owner

    @is_owner.setter
    def is_owner(self, value: bool) -> None:
        self._is_owner = value
        self._draw_image()
        return None

    pass
