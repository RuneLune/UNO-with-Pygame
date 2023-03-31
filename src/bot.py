from __future__ import annotations

import random

from player import Player
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Bot(Player):
    # Bot 클래스 생성자
    def __new__(cls, *args, **kwargs):
        return super(Bot, cls).__new__(cls)

    # Bot 객체 초기화 메서드
    def __init__(self, game: Game, name: str) -> None:
        return super(Bot, self).__init__(game, name)

    # turn_start 오버라이딩
    def turn_start(self) -> None:
        super().turn_start()
        self.__play()
        return None

    # 자동으로 턴을 진행하는 메서드
    def __play(self) -> None:
        if len(self.__discardable_cards_index):
            self.discard_card(random.choice(self.__discardable_cards_index))
            pass
        else:
            discarded_card_info = self.__game.get_discard_info()
            force_draw: int = discarded_card_info.get("force_draw")
            if force_draw > 0:
                self.draw_cards(force_draw)
                pass
            else:
                self.draw_cards(1)
                pass
            pass
        return None

    # ask_discard 오버라이딩
    def ask_discard(self) -> None:
        self.discard_card(-1)
        return None

    # choose_color 오버라이딩
    def choose_color(self) -> None:
        self.__game.set_color(random.choice([1, 2, 3, 4]))
        return None
