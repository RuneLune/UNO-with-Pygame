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


class StartButton(TextObject, Subject):
    _observers: List[Type[Observer]] = []

    def __init__(self) -> None:
        return super(StartButton, self).__init__(
            "Goto scene2",
            pygame.font.Font(font_resource("MainFont.ttf"), 30),
            colors.white,
            "Scene1_StartButton",
            -1,
            -1,
            10,
            10,
            999,
        )

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
