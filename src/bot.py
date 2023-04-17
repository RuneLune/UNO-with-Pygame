from __future__ import annotations

from overrides import overrides
import random
from timer import Timer
from typing import TYPE_CHECKING, Dict, Type

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
    def __init__(self, game: Type[Game], name: str = "Computer") -> None:
        super(Bot, self).__init__(game, name)
        self._timer: Timer = Timer()
        self._timer.start()
        self._delay = 0
        return None

    # turn_start 오버라이딩
    @overrides
    def turn_start(self) -> None:
        super(Bot, self).turn_start()
        self._delay = random.uniform(0.5, 1.5)
        self._timer.start()
        # self._play()
        return None

    @overrides
    def tick(self) -> None:
        if self._turn is True:
            if self._timer.get().total_seconds() > self._delay:
                self._play()
                self._timer.stop()
                pass
            pass
        return None

    @overrides
    def pause_timer(self) -> None:
        self._timer.pause()
        return None

    @overrides
    def resume_timer(self) -> None:
        self._timer.resume()
        return None

    # 자동으로 턴을 진행하는 메서드
    def _play(self) -> None:
        if len(self._discardable_cards_index):
            self.discard_card(random.choice(self._discardable_cards_index))
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

    # ask_discard 오버라이딩
    @overrides
    def ask_discard(self) -> None:
        self._check_discardable_cards()
        self.discard_card(-1)
        return None

    # choose_color 오버라이딩
    @overrides
    def choose_color(self) -> None:
        self.set_color(random.randrange(1, 5))
        return None
