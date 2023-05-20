from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING, List, Type

import pygame

from abstrclass.observer import Observer
from abstrclass.subject import Subject
from manager.cfgmgr import Config
from gameobj.gameobj import GameObject
from metaclass.singleton import SingletonMeta

from gameobj.ingame.selector import Selector


class KeyInput(GameObject, Observer):
    @overrides
    def start(self) -> None:
        self.object_list = []
        self.card_index = 0
        self.vertical_index = 0
        self.color_choice = False
        self.color_index = 0

    def observer_update(self, subject: Type[Subject]) -> None:
        self.user = subject.get_user()

    @overrides
    def on_key_down(self, key: int) -> bool:
        keyconfig_value = Config().config.get("keybindings")
        if self.color_choice is False:
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
                if self.vertical_index == 0:
                    self.vertical_index = 1
                    self.object_list[self.card_index].on_mouse_exit()
                    self.uno_btn.on_mouse_enter()
                elif self.vertical_index == 1:
                    self.vertical_index = 2
                    self.uno_btn.on_mouse_exit()
                    self.deck_card.on_mouse_enter()
                elif self.vertical_index == 2:
                    None
            elif key == keyconfig_value.get("down"):
                if self.vertical_index == 2:
                    self.vertical_index = 1
                    self.deck_card.on_mouse_exit()
                    self.uno_btn.on_mouse_enter()
                elif self.vertical_index == 1:
                    self.vertical_index = 0
                    self.uno_btn.on_mouse_exit()
                    self.object_list[self.card_index].on_mouse_enter()
                elif self.vertical_index == 0:
                    None
            elif key == keyconfig_value.get("select"):
                if self.vertical_index == 0:
                    if self.card_index == 0:
                        self.object_list[self.card_index].on_mouse_down()
                    else:
                        self.object_list[self.card_index].on_mouse_down()
                        self.card_index = (self.card_index - 1) % len(self.object_list)
                elif self.vertical_index == 1:
                    self._selector.center = self.uno_btn.center
                    self.uno_btn.on_mouse_down()
                elif self.vertical_index == 2:
                    self._selector.center = self.deck_card.center
                    self.deck_card.on_mouse_down()
                pass
            elif key == keyconfig_value.get("cancel"):
                pass
        else:
            if key == keyconfig_value.get("up"):
                self.color_rect[self.color_index].on_mouse_exit()
                self.color_index = (self.color_index - 1) % len(self.color_rect)
                self.color_rect[self.color_index].on_mouse_enter()
                pass
            elif key == keyconfig_value.get("down"):
                self.color_rect[self.color_index].on_mouse_exit()
                self.color_index = (self.color_index + 1) % len(self.color_rect)
                self.color_rect[self.color_index].on_mouse_enter()
            elif key == keyconfig_value.get("select"):
                self.color_rect[self.color_index].on_mouse_down()
                self.color_choice = False

        return False

    def attach_card(self, card, deck, uno, color_rect):
        self.object_list = card
        self.deck_card = deck
        self.uno_btn = uno
        self.color_rect = color_rect

    def attach_selector(self, selector: Type[Selector]) -> KeyInput:
        self._selector = selector
        return self

    def state_update(self):
        if self.user._discarded_wild is True and self.user.is_turn() is True:
            self.color_choice = True
        else:
            self.color_choice = False

    @overrides
    def update(self) -> None:
        if len(self.object_list) == 0:
            return None
        if self.color_choice is True:
            self._selector.center = self.color_rect[self.color_index].center
        else:
            if self._selector is not None and self.vertical_index == 0:
                self._selector.center = self.object_list[self.card_index].center
            elif self._selector is not None and self.vertical_index == 1:
                self._selector.center = self.uno_btn.center
            elif self._selector is not None and self.vertical_index == 2:
                self._selector.center = self.deck_card.center
