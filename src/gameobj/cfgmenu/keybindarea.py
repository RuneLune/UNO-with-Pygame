from __future__ import annotations

from overrides import overrides
import pygame

from ..txtbtnobj import TextButtonObject
from .keyinput import KeyInput
import util.colors as color


class KeyBindArea(TextButtonObject):
    Inst_created: int = 0
    Insts: list[KeyBindArea] = []

    def __new__(cls, *args, **kwargs):
        cls.Inst_created += 1
        return super().__new__(cls)

    @overrides
    def start(self) -> None:
        KeyBindArea.Insts.append(self)
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect = pygame.Rect(
            screen_rect.width * 4 // 8,
            screen_rect.height * (6 + KeyBindArea.Inst_created) // 16,
            screen_rect.width // 4,
            screen_rect.height // 16,
        )
        self.target_config = self.text
        self.text = None
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(color.white)
        self.alpha = 0
        self.image.set_alpha(255)
        self.z_index = 800
        pass

    @overrides
    def on_click(self) -> None:
        KeyInput().configuring_key = self.target_config
        return None

    @overrides
    def update(self) -> None:
        if self._mouse_over:
            self.alpha += 5
            if self.alpha > 50:
                self.alpha = 50
                pass
            pass
        else:
            self.alpha -= 5
            if self.alpha < 0:
                self.alpha = 0
                pass
            pass
        self.image.set_alpha(self.alpha)
        return None

    @overrides
    def on_destroy(self) -> None:
        KeyBindArea.Inst_created -= 1
        return None

    @overrides
    def on_mouse_enter(self) -> None:
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        return None

    @staticmethod
    def destroy_all() -> None:
        for inst in KeyBindArea.Insts:
            inst.on_destroy()
            del inst
            pass
        KeyBindArea.Inst_created = 0
        return None

    pass
