import random
from overrides import overrides
from typing import Final

from game import Game
from player import Player
from bot import Bot


class Stage_A(Game):
    # Stage_A 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(Stage_A, cls).__new__(cls)

    # Stage_A 객체 초기화 메서드
    @overrides
    def __init__(self, username: str = "Player") -> None:
        self._init_variables(10, 0, 1, 0)
        self._add_players()
        self._make_draw_pile()
        self._deal_hands()
        self._flip_top()

        self._players[self._current_turn].turn_start()

        return None

    @overrides
    def _add_players(self, username: str = "Player", players_count: int = 4) -> None:
        self._user: Player = Player(self, username)
        self._computer: Bot = Bot(self, "Computer 1")
        self._players.append(self._user)
        self._players.append(self._computer)
        random.shuffle(self._players)
        return None

    @overrides
    def _deal_hands(self, count: int = 7) -> None:
        chance: Final[int] = 0.6
        normal_count: int = 0
        functional_count: int = 0
        for i in range(0, count):
            random_number = random.random()
            if random_number < chance:
                functional_count += 1
                pass
            else:
                normal_count += 1
                pass
            continue
        self._draw_normal_card(self._computer, normal_count)
        self._draw_functional_card(self._computer, functional_count)
        self._user.draw_cards(count)

        return None

    # 기술 카드 드로우 메서드
    def _draw_functional_card(self, player: Player | Bot, count: int = 1) -> None:
        draw_count: int = 0
        for card in self._draw_pile:
            if card % 100 < 10:
                continue
            else:
                player.get_cards([card])
                draw_count += 1
                self._draw_pile.remove(card)
                pass
            if draw_count >= count:
                break
            else:
                continue

        return None

    # 일반 카드 드로우 메서드
    def _draw_normal_card(self, player: Player | Bot, count: int = 1) -> None:
        draw_count: int = 0
        for card in self._draw_pile:
            if card % 100 < 10:
                player.get_cards([card])
                draw_count += 1
                self._draw_pile.remove(card)
                pass
            else:
                continue
            if draw_count >= count:
                break
            else:
                continue

        return None
