from __future__ import annotations

from overrides import overrides
from typing import TYPE_CHECKING, Type, List, Dict
import copy
import random

from player.bot import Bot
import card.cards as cards

if TYPE_CHECKING:
    from game.game import Game


class Combo_Bot(Bot):
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(Combo_Bot, cls).__new__(cls)

    @overrides
    def __init__(self, game: Type[Game], name: str = "Computer") -> None:
        return super(Combo_Bot, self).__init__(game, name)

    @overrides
    def _play(self) -> None:
        if self._discardable_cards_index:
            if len(self._cards) == 2:
                self.yell_uno()
                pass
            self.build_combo()
            if self._max_combo:
                self.discard_card(self._cards.index(self._max_combo[0]))
                pass
            else:
                self.discard_card(random.choice(self._discardable_cards_index))
                pass
            pass
        else:
            discarded_card_info: Dict[
                str, int | Dict[str, str | int]
            ] = self._game.get_discard_info()
            force_draw: int = discarded_card_info.get("force_draw")
            if force_draw > 0:
                self.draw_cards(force_draw)
                pass
            else:
                self.draw_cards(1)
                pass
            pass
        return None

    def build_combo(self) -> None:
        self._max_combo = []
        self._combo_list = []
        hand = []
        for card in self._cards:
            if (
                cards.check_card(card).get("type") == "draw2"
                or cards.check_card(card).get("type") == "skip"
            ):
                hand.append(card)
                pass
            continue
        last_card = self._game.get_discard_info().get("discarded_card")
        for card in hand:
            card_info = cards.check_card(card)
            if card_info.get("color") == last_card.get("color") or card_info.get(
                "type"
            ) == last_card.get("type"):
                temp_list = copy.deepcopy(hand)
                temp_list.remove(card)
                self._build_combo([card], temp_list)
                pass
            continue
        self._max_combo = []
        for combo in self._combo_list:
            if len(combo) > len(self._max_combo):
                self._max_combo = combo
                pass
            continue
        return None

    def _build_combo(self, combo: List[int], hand: List[int]) -> None:
        last_card = cards.check_card(combo[-1])
        if hand:
            for card in hand:
                card_info = cards.check_card(card)
                if card_info.get("color") == last_card.get("color") or card_info.get(
                    "type"
                ) == last_card.get("type"):
                    temp_list = copy.deepcopy(hand)
                    temp_list.remove(card)
                    self._build_combo(copy.deepcopy(combo) + [card], temp_list)
                    pass
                continue
            pass
        self._combo_list.append(combo)
        return None
