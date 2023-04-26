from __future__ import annotations

from overrides import overrides
from typing import Type, List, TYPE_CHECKING
import pygame

from ..textobj import TextObject
from abstrclass.subject import Subject
from util.resource_manager import font_resource
import util.colors as colors

if TYPE_CHECKING:
    from abstrclass.observer import Observer


class StageButton(TextObject, Subject):
    _observers: List[Type[Observer]] = []

    def __init__(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        return super(StageButton, self).__init__(
            "Stage",
            pygame.font.Font(font_resource("MainFont.ttf"), screen_rect.height // 12),
            colors.black,
            "MainMenu_StageButton",
            -1,
            -1,
            10,
            10,
            999,
        )

    @overrides
    def start(self) -> None:
        screen_rect = self._screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.height * 7 // 10
        return None

    @overrides
    def on_mouse_enter(self) -> None:
        self.image = self.font.render(self.text, True, colors.red)
        return None

    @overrides
    def on_mouse_exit(self) -> None:
        self.image = self.font.render(self.text, True, self.color)
        return None

    @overrides
    def on_mouse_up_as_button(self) -> None:
        self.target_scene = "scene2"
        self.notify()
        return None

    @overrides
    def attach(self, observer: Type[Observer]) -> None:
        self._observers.append(observer)
        return None

    @overrides
    def detach(self, observer: Type[Observer]) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
        return None

    @overrides
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)
            continue
        return None

    pass
