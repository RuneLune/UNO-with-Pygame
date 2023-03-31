import copy
from typing import List

import cards
from game import Game


class Player:
    # Player 클래스 생성자
    def __new__(cls, *args, **kwargs):
        return super(Player, cls).__new__(cls, *args, **kwargs)

    # Player 객체 초기화 메서드
    def __init__(self, game: Game, name: str) -> None:
        self.__game = game
        self.__name = name
        self.__cards = []
        self.__turn = False
        self.__yelled_uno = False
        self.__points = 0
        return super(Player, self).__init__()

    # Draw pile로부터 count만큼 카드를 뽑아오는 메서드
    def draw_cards(self, count: int) -> None:
        self.__game.draw_cards(count, self)
        return None

    # 플레이어에게 cards_list에 있는 카드를 주는 메서드
    def get_cards(self, cards_list: List[int]) -> None:
        self.__cards += cards_list
        self.__cards.sort()
        return None

    # (주의) 플레이어의 기존 카드를 없애고 카드를 cards_list로 설정하는 메서드
    def set_cards(self, cards_list: List[int]) -> None:
        self.__cards = copy.deepcopy(cards_list)
        return None

    # 플레이어의 이름을 반환하는 메서드
    def get_name(self) -> str:
        return self.__name

    # 플레이어가 이번 턴에 우노를 외친 여부를 반환하는 메서드
    def is_uno(self) -> bool:
        return self.__yelled_uno

    # 플레이어가 현재 가지고 있는 카드를 반환하는 메서드
    def get_hand_cards(self) -> List[int]:
        return copy.deepcopy(self.__cards)

    # 플레이어의 턴 시작 시 호출되는 메서드
    def turn_start(self) -> None:
        self.__turn = True
        self.__check_discardable_cards()
        return None

    # 플레이어의 턴 종료 시 호출되는 메서드
    def turn_end(self) -> None:
        self.__turn = False
        self.__game.next_turn()
        return None

    # 플레이어의 현재 점수를 points만큼 추가하는 메서드
    def add_points(self, points: int) -> None:
        self.__points += points
        return None

    # 플레이어의 현재 점수를 반환하는 메서드
    def get_points(self) -> int:
        return self.__points

    # 플레이어가 낼 수 있는 카드의 인덱스를 확인하는 메서드
    def __check_discardable_cards(self) -> None:
        discard_info = self.__game.get_discard_info()
        self.__discardable_cards_index = []
        if discard_info.get("force_draw") > 0:
            return None
        else:
            discarded_card = discard_info.get("discarded_card")
            for i in range(0, len(self.__cards)):
                card = cards.check_card(self.__cards[i])
                if card.get("color") == discarded_card.get("color") or card.get(
                    "number"
                ) == discarded_card.get("number"):
                    self.__discardable_cards_index.append(i)
        return None

    # 플레이어가 낼 수 있는 카드의 인덱스를 반환하는 메서드
    def get_discardable_cards_index(self) -> List[int]:
        return copy.deepcopy(self.__discardable_cards_index)

    # 플레이어가 가진 카드의 리스트에서 index의 카드를 내는 메서드
    def discard_card(self, index: int) -> None:
        self.__game.discard_card(self.__cards[index])
        del self.__cards[index]
        return None

    # ??
    def end_turn(self) -> None:
        self.__game.end_turn()
        return None

    # def choose_color(self):
    #     self.__game.set_color()

    # def ask_discard(self):
