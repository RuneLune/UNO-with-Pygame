from overrides import overrides
import random

from game.game import Game


class Stage_C(Game):
    # Stage_C 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(Stage_C, cls).__new__(cls)

    # Stage_C 객체 초기화 메서드
    @overrides
    def __init__(self, username: str = "Player") -> None:
        self._init_variables(10, 0, 1, 0)
        self._add_players(username, 3)
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
        return super(Stage_C, self)._init_variables(
            turn_seconds, round_seconds, max_rounds, target_score
        )

    @overrides
    def end_turn(self) -> None:
        self._truns_count += 1
        if self._truns_count % 5 == 0:
            self._discarded_card.update(
                color=random.choice(["blue", "green", "red", "yellow"])
            )
        return super(Stage_C, self).end_turn()
