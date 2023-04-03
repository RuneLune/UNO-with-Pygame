from __future__ import annotations

from overrides import overrides
import random
from typing import TYPE_CHECKING, Dict, List

from player import Player

if TYPE_CHECKING:
    from game import Game


class Bot(Player):
    # Bot 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(Bot, cls).__new__(cls)

    # Bot 객체 초기화 메서드
    @overrides
    def __init__(self, game: Game, name: str = "Computer") -> None:
        super(Bot, self).__init__(game, name)
        self.__game: Game = super(Bot, self).get_game()
        return None

    # turn_start 오버라이딩
    @overrides
    def turn_start(self) -> None:
        super(Bot, self).turn_start()
        self.__discardable_cards_index: List[int] = super(
            Bot, self
        ).get_discardable_cards_index()
        self.__play()
        return None

    # 자동으로 턴을 진행하는 메서드
    def __play(self) -> None:
        if len(self.__discardable_cards_index):
            self.discard_card(random.choice(self.__discardable_cards_index))
            pass
        else:
            discarded_card_info: Dict[str, int | Dict[str, str | int]] = (
                super(Bot, self).get_game().get_discard_info()
            )
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
    @overrides
    def ask_discard(self) -> None:
        self.discard_card(-1)
        return None

    # choose_color 오버라이딩
    @overrides
    def choose_color(self) -> None:
        self.__game.set_color(random.choice([1, 2, 3, 4]))
        return None
