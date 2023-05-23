import random
from overrides import overrides
from typing import Type

import card.cards as cards
from game.game import Game
from player.player import Player
from player.combo_bot import ComboBot


class StageA(Game):
    # StageA 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(StageA, cls).__new__(cls)

    # StageA 객체 초기화 메서드
    @overrides
    def __init__(self, players_count: int = 2, username: str = "User") -> None:
        self._init_variables(10, 0, 1, 0)
        self._add_players(username, players_count)
        self._make_draw_pile()
        self._deal_hands()
        self._flip_top()
        self.start_timer()

        # self._user.set_cards([cards.wild_normal] * 3)
        # self._computer.set_cards([cards.blue_draw2, cards.red_draw2, cards.yellow_draw2, cards.green_draw2, cards.blue_0, cards.yellow_0])
        self._players[self._current_turn].turn_start()
        self._name = "stage_a"

        return None

    @overrides
    def _add_players(self, username: str = "User", players_count: int = 4) -> None:
        self._user: Player = Player(self, username)
        self._bots: list[ComboBot] = []
        self._players.append(self._user)
        for i in range(1, players_count):
            bot = ComboBot(self, "CPU " + str(i))
            self._players.append(bot)
            self._bots.append(bot)
            continue
        random.shuffle(self._players)
        return None

    @overrides
    def _deal_hands(self, count: int = 7) -> None:
        for bot in self._bots:
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
                random_number = random.randrange(
                    0, normal_cards * 2 + functional_cards * 3
                )
                if random_number < normal_cards * 2:
                    normal_draw += 1
                    normal_cards -= 1
                    pass
                else:
                    functional_draw += 1
                    functional_cards -= 1
                    pass
                continue
            self._draw_normal_card(bot, normal_draw)
            self._draw_functional_card(bot, functional_draw)
            continue
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
    def _draw_normal_card(self, player: Type[Player], count: int = 1) -> None:
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
