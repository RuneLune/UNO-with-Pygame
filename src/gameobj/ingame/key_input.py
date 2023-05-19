from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING, List, Type

import pygame

from abstrclass.observer import Observer
from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta

from gameobj.ingame.selector import Selector


class KeyInput(GameObject, Observer):
    @overrides
    def start(self) -> None:
        self.object_list = []
        self.card_index = 0
        self.deck_card = None
        self.space_index = 0

    @overrides
    def on_key_down(self, key: int) -> bool:
        keyconfig_value = Config().config.get("keybindings")
        if key == keyconfig_value.get("left"):
            self.object_list[self.card_index].on_mouse_exit()
            self.card_index = (self.card_index - 1) % len(self.object_list)
            self.object_list[self.card_index].on_mouse_enter()
            pass
        elif key == keyconfig_value.get("right"):
            self.object_list[self.card_index].on_mouse_exit()
            self.card_index = (self.card_index + 1) % len(self.object_list)
            self.object_list[self.card_index].on_mouse_enter()
            pass
        elif key == keyconfig_value.get("up"):
            self.object_list[self.card_index].on_mouse_exit()
            self.space_index = 1
            self.deck_card.on_mouse_enter()
            pass
        elif key == keyconfig_value.get("down"):
            self.deck_card.on_mouse_exit()
            self.space_index = 0
            self.object_list[self.card_index].on_mouse_enter()
            pass
        elif key == keyconfig_value.get("select"):
            if self.space_index == 0:
                if self.card_index == 0:
                    self.object_list[self.card_index].on_mouse_down()
                else:
                    self.object_list[self.card_index].on_mouse_down()
                    self.card_index = (self.card_index - 1) % len(self.object_list)
            elif self.space_index == 1:
                self.card_index = (self.card_index - 1) % len(self.object_list)
                self._selector.center = self.object_list[self.card_index].center
                self.deck_card.on_mouse_down()
            pass
        elif key == keyconfig_value.get("cancel"):
            pass

        return False

    def attach_card(self, card, deck):
        self.object_list = card
        self.deck_card = deck

    def attach_selector(self, selector: Type[Selector]) -> KeyInput:
        self._selector = selector
        return self

    # def on_index_change(self) -> None:
    #     if self._selector is not None:
    #         self._selector.center = self.object_list[self.card_index].center
    #     return None

    @overrides
    def update(self) -> None:
        if self._selector is not None and self.space_index == 0:
            self._selector.center = self.object_list[self.card_index].center
        elif self._selector is not None and self.space_index == 1:
            self._selector.center = self.deck_card.center
