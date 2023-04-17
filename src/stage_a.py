import random
from overrides import overrides
from typing import Type

import cards
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
        normal_cards: int = 0
        functional_cards: int = 0
        for card in self._draw_pile:
            if cards.check_card(card).get("type") == "normal":
                normal_cards += 1
                pass
            else:
                functional_cards += 1
                pass
            continue
        normal_draw: int = 0
        functional_draw: int = 0
        for i in range(0, count):
            random_number = random.randrange(0, normal_cards * 2 + functional_cards * 3)
            if random_number < normal_cards * 2:
                normal_draw += 1
                normal_cards -= 1
                pass
            else:
                functional_draw += 1
                functional_cards -= 1
                pass
            continue
        self._draw_normal_card(self._computer, normal_draw)
        self._draw_functional_card(self._computer, functional_draw)
        self._user.draw_cards(count)

        return None

    # 기술 카드 드로우 메서드
    def _draw_functional_card(self, player: Type[Player], count: int = 1) -> None:
        draw_count: int = 0
        for card in self._draw_pile:
            if draw_count >= count:
                break
            elif card % 100 < 10:
                pass
            else:
                player.get_cards([card])
                draw_count += 1
                self._draw_pile.remove(card)
                pass
            continue

        return None

    # 일반 카드 드로우 메서드
    def _draw_normal_card(self, player: Player | Bot, count: int = 1) -> None:
        draw_count: int = 0
        for card in self._draw_pile:
            if draw_count >= count:
                break
            elif card % 100 < 10:
                player.get_cards([card])
                draw_count += 1
                self._draw_pile.remove(card)
                pass
            else:
                pass
            continue

        return None
