from overrides import overrides
import random

from game.game import Game


class StageC(Game):
    # StageC 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(StageC, cls).__new__(cls)

    # StageC 객체 초기화 메서드
    @overrides
    def __init__(self, players_count: int = 3, username: str = "User") -> None:
        self._init_variables(10, 0, 1, 0)
        self._add_players(username, players_count)
        self._make_draw_pile()
        self._deal_hands()
        self._flip_top()
        self.start_timer()

        self._players[self._current_turn].turn_start()
        self._name = "stage_c"

        return None

    @overrides
    def _init_variables(
        self,
        turn_seconds: int = 10,
        round_seconds: int = 0,
        max_rounds: int = 0,
        target_score: int = 500,
    ) -> None:
        self._truns_count = 0
        return super(StageC, self)._init_variables(
            turn_seconds, round_seconds, max_rounds, target_score
        )

    @overrides
    def end_turn(self) -> None:
        self._truns_count += 1
        if self._truns_count % 5 == 0:
            self._discarded_card.update(
                color=random.choice(["blue", "green", "red", "yellow"])
            )
        return super(StageC, self).end_turn()
