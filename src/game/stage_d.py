from game.game import Game
from overrides import overrides
from typing import Type

from player.player import Player


class StageD(Game):
    @overrides
    def __init__(self, players_count: int = 2, username: str = "User") -> None:
        super(StageD, self).__init__(2)
        self._name = "stage_d"
        return None

    @overrides
    def draw_cards(
        self, count: int, player: Type[Player], check_force_draw: bool = True
    ) -> None:
        if player is self._user and self._force_draw <= 0 and count == 1:
            count = 2
            pass
        return super().draw_cards(count, player, check_force_draw)
