import random
from overrides import overrides
from typing import Final

from game import Game
from player import Player
from bot import Bot


class Stage_01(Game):
    # Stage_01 클래스 생성자
    @overrides
    def __new__(cls, *args, **kwargs):
        return super(Stage_01, cls).__new__(cls)

    # Stage_01 객체 초기화 메서드
    @overrides
    def __init__(self, username: str = "Player") -> None:
        self.__init_variables(10, 0, 1, 0)

        # 봇 및 플레이어 추가
        self.__user: Player = Player(self, username)
        self.__computer: Bot = Bot(self, "Computer 1")
        self.__players.append(self.__user)
        self.__players.append(self.__computer)
        random.shuffle(self.__players)

        self.__make_draw_pile()
        self.__deal_hands()
        self.__flip_top()

        self.__players[self.__current_turn].turn_start()

        return None

    @overrides
    def __deal_hands(self, count: int = 7) -> None:
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
        self.__draw_normal_card(self.__computer, normal_count)
        self.__draw_functional_card(self.__computer, functional_count)
        self.__user.draw_cards(count)

        return None

    # 기술 카드 드로우 메서드
    def __draw_functional_card(self, player: Player | Bot, count: int = 1) -> None:
        draw_count: int = 0
        for card in self.__draw_pile:
            if card % 100 < 10:
                continue
            else:
                player.get_cards([card])
                draw_count += 1
                self.__draw_pile.remove(card)
                pass
            if draw_count >= count:
                break
            else:
                continue

        return None

    # 일반 카드 드로우 메서드
    def __draw_normal_card(self, player: Player | Bot, count: int = 1) -> None:
        draw_count: int = 0
        for card in self.__draw_pile:
            if card % 100 < 10:
                player.get_cards([card])
                draw_count += 1
                self.__draw_pile.remove(card)
                pass
            else:
                continue
            if draw_count >= count:
                break
            else:
                continue

        return None
