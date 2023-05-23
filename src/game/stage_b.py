from overrides import overrides
from typing import List
import random

from game.game import Game
import card.cards as cards


class StageB(Game):
    # StageB 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(StageB, cls).__new__(cls)

    # StageB 객체 초기화 메서드
    @overrides
    def __init__(self, players_count: int = 4, username: str = "User") -> None:
        self._init_variables(10, 0, 1, 0)
        self._add_players(username, players_count)
        self._make_draw_pile()
        drawing_cards_count: int = (len(self._draw_pile) - 1) // len(self._players)
        self._deal_hands(drawing_cards_count)
        self._flip_top()
        self.start_timer()

        self._players[self._current_turn].turn_start()
        self._name = "stage_b"

        return None

    @overrides
    def _make_draw_pile(self) -> None:
        self._draw_pile: List[int] = (
            list(range(cards.blue_0, cards.blue_skip + 1))
            + list(range(cards.green_0, cards.green_skip + 1))
            + list(range(cards.red_0, cards.red_skip + 1))
            + list(range(cards.yellow_0, cards.yellow_skip + 1))
            + list(range(cards.wild_normal, cards.wild_draw4 + 1))
            + [cards.wild_shuffle]
            + [cards.wild_custom]
        )
        random.shuffle(self._draw_pile)
        return None
