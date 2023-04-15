from __future__ import annotations

import copy
import pygame
from typing import List, Iterable, TYPE_CHECKING, Dict, Type

import cards
import events

if TYPE_CHECKING:
    from game import Game


class Player:
    # Player 클래스 생성자
    def __new__(cls, *args, **kwargs):
        return super(Player, cls).__new__(cls)

    # Player 객체 초기화 메서드
    def __init__(self, game: Type[Game], name: str = "Player") -> None:
        self._game: Type[Game] = game
        self._name: str = name
        self._cards: list[int] = []
        self._turn: bool = False
        self._yelled_uno: bool = False
        self._points: int = 0
        self._discardable_cards_index = []
        self._can_end_turn = False
        return super(Player, self).__init__()

    def tick(self) -> None:
        return None

    # Draw pile로부터 count만큼 카드를 뽑아오는 메서드
    def draw_cards(self, count: int = -1) -> None:
        if count == -1:
            if self._turn is False:
                return None
            if self._game.get_discard_info().get("force_draw") > 0:
                count = self._game.get_discard_info().get("force_draw")
                pass
            else:
                count = 1
        self._game.draw_cards(count, self)
        self._can_end_turn = True
        self._cards.sort()
        if self._turn is True:
            self.end_turn()
        return None

    # 플레이어에게 cards_list에 있는 카드를 주는 메서드
    def get_cards(self, cards_list: Iterable[int]) -> None:
        self._cards += list(cards_list)
        return None

    # (주의) 플레이어의 기존 카드를 없애고 카드를 cards_list로 설정하는 메서드
    def set_cards(self, cards_list: Iterable[int]) -> None:
        self._cards = list(cards_list)
        return None

    # 플레이어의 이름을 반환하는 메서드
    def get_name(self) -> str:
        return self._name

    # 플레이어가 이번 턴에 우노를 외친 여부를 반환하는 메서드
    def is_uno(self) -> bool:
        return self._yelled_uno

    # 플레이어가 현재 가지고 있는 카드를 반환하는 메서드
    def get_hand_cards(self) -> List[int]:
        return copy.deepcopy(self._cards)

    # 플레이어의 턴 시작 시 호출되는 메서드
    def turn_start(self) -> None:
        self._turn = True
        self._can_end_turn = False
        self._check_discardable_cards()
        return None

    # 플레이어의 현재 점수를 points만큼 추가하는 메서드
    def add_points(self, points: int) -> None:
        self._points += points
        return None

    # 플레이어의 현재 점수를 반환하는 메서드
    def get_points(self) -> int:
        return self._points

    # 플레이어가 낼 수 있는 카드의 인덱스를 확인하는 메서드
    def _check_discardable_cards(self) -> None:
        discard_info: Dict[
            str, int | Dict[str, str | int]
        ] = self._game.get_discard_info()
        self._discardable_cards_index = []
        if discard_info.get("force_draw") > 0:
            pass
        else:
            discarded_card: Dict[str, str | int] = discard_info.get("discarded_card")
            for i in range(0, len(self._cards)):
                card: Dict[str, str | int] = cards.check_card(self._cards[i])
                if card.get("color") == discarded_card.get("color") or (
                    card.get("number") == discarded_card.get("number")
                ):
                    self._discardable_cards_index.append(i)
        return None

    # 플레이어가 낼 수 있는 카드의 인덱스를 반환하는 메서드
    def get_discardable_cards_index(self) -> List[int]:
        self._check_discardable_cards()
        return copy.deepcopy(self._discardable_cards_index)

    # 플레이어가 가진 카드의 리스트에서 index의 카드를 내는 메서드
    def discard_card(self, index: int) -> None:
        if self._turn is False:
            print("Not user's turn")
            return None
        # print(self._cards)
        # print(self._discardable_cards_index)
        if index not in self._discardable_cards_index:
            print("Selected non-discardable card. ")
            return None
        self._discardable_cards_index.remove(index % len(self._cards))
        self._game.discard_card(self._cards[index])
        self._can_end_turn = True
        del self._cards[index]
        self.end_turn()
        return None

    # 플레이어가 뽑은 카드가 낼 수 있는 경우 물어보는 메서드
    def ask_discard(self) -> None:
        return None

    # 플레이어의 턴 종료 시 호출되는 메서드
    def end_turn(self) -> None:
        self._turn = False
        self._game.end_turn()
        self._can_end_turn = False
        self._cards.sort()
        return None

    # 와일드 카드를 냈을 때 호출되는 메서드
    def choose_color(self) -> None:
        pygame.event.post(pygame.event.Event(events.ASK_COLOR))
        return None

    # 색을 정하는 메서드
    def set_color(self, color: int | str) -> None:
        self._game.set_color(color)
        return None
