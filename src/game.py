import random
import copy
from typing import List, Dict, Iterable

import cards
from player import Player
from bot import Bot
from timer import Timer


class Game:
    # MAX_Inst = 1
    # Inst_created = 0

    # Game 클래스 생성자
    def __new__(cls, *args, **kwargs):
        # if cls.Inst_created >= cls.MAX_Inst:
        #     raise ValueError("Cannot create more Game object")
        # cls.Inst_created += 1
        return super(Game, cls).__new__(cls)

    # Game 객체 초기화 메서드
    def __init__(
        self,
        players_count: int,
        turn_seconds: int = 10,
        round_seconds: int = -1,
        max_rounds: int = -1,
        target_score: int = 500,
    ) -> None:
        # 봇 및 플레이어 추가
        self.__players = []
        for i in range(0, players_count - 1):
            self.__players.append(Bot(self, "Bot " + str(i + 1)))
        self.__players.append(Player(self, "Player"))
        random.shuffle(self.__players)

        self.__turn_timer = Timer()
        self.__round_timer = Timer()

        self.__turn_seconds = turn_seconds
        self.__round_seconds = round_seconds
        self.__max_rounds = max_rounds
        self.__target_score = target_score

        self.__force_draw = 0
        self.__reverse_direction = False
        self.__current_turn = 1
        self.__skip_turn = False

        # 카드 추가, 셔플 및 패 분배
        self.__draw_pile = (
            list(range(cards.blue_0, cards.blue_skip + 1))
            + list(range(cards.blue_1, cards.blue_skip + 1))
            + list(range(cards.green_0, cards.green_skip + 1))
            + list(range(cards.green_1, cards.green_skip + 1))
            + list(range(cards.red_0, cards.red_skip + 1))
            + list(range(cards.red_1, cards.red_skip + 1))
            + list(range(cards.yellow_0, cards.yellow_skip + 1))
            + list(range(cards.yellow_1, cards.yellow_skip + 1))
            + list(range(cards.wild_normal, cards.wild_draw4 + 1)) * 4
        )
        random.shuffle(self.__draw_pile)
        for i in range(0, len(self.__players)):
            self.__players[i].draw_cards(7)

        # 패산에서 한 장 뒤집기
        self.__discard_pile = self.__draw_pile[:1]
        self.__draw_pile = self.__draw_pile[1:]
        self.__discarded_card = cards.check_card(self.__discard_pile[0])

        # 4장 드로우 카드는 덱으로 되돌리고 다시 뒤집기
        while self.__discarded_card.get("type", None) == "draw4":
            self.__draw_pile += self.__discard_pile
            self.__discard_pile = self.__draw_pile[:1]
            self.__draw_pile = self.__draw_pile[1:]
            self.__discarded_card = cards.check_card(self.__discard_pile[0])

        # 기술카드 처리
        if self.__discarded_card.get("type", None) == "draw2":
            self.__force_draw = 2
        elif self.__discarded_card.get("type", None) == "reverse":
            self.__current_turn = 0
            self.__reverse_direction = True
        elif self.__discarded_card.get("type", None) == "skip":
            self.__current_turn = 2 % len(self.__players)
        elif self.__discarded_card.get("color", None) == "wild":
            self.__players[1].choose_color(self)

        self.__player_drawed = False

        return super().__init__()

    # Discard pile에 있는 카드를 섞고 Draw pile에 추가하는 메서드
    def __shuffle(self) -> None:
        discarded_cards = self.__discard_pile[1:]
        random.shuffle(discarded_cards)
        self.__draw_pile += discarded_cards
        self.__discard_pile = self.__discard_pile[:1]
        return None

    # 마지막으로 낸 카드 정보를 반환하는 메서드
    def get_discard_info(self) -> Dict[str, int | List[int]]:
        return {
            "force_draw": self.__force_draw,
            "discarded_card": copy.deepcopy(self.__discarded_card),
        }

    # player에게 Draw pile에서 count만큼 카드를 주는 메서드
    def draw_cards(self, count: int, player: Player | Bot) -> None:
        # 강제 드로우 수 확인
        if self.__force_draw > 0:
            if count != self.__force_draw:
                raise ValueError("must draw " + self.__force_draw + " cards")

        # 남은 카드가 부족하면 패 섞고 드로우
        if count >= len(self.__draw_pile):
            self.__shuffle()
        drawing_cards = copy.deepcopy(self.__draw_pile[:count])
        self.__draw_pile = self.__draw_pile[count:]
        player.get_cards(drawing_cards)
        self.__player_drawed = True
        # 뽑은 카드가 낼 수 있는 경우 처리(미구현)
        if len(drawing_cards) == 1:
            draw_card = cards.check_card(drawing_cards[0])
            if (
                draw_card.get("color") == "wild"
                or draw_card.get("color") == self.__discarded_card.get("color")
                or draw_card("number") == self.__discarded_card.get("number")
            ):
                self.__players[self.__current_turn].ask_discard()
        self.__force_draw = 0
        return None

    # card를 Discard pile에 추가하고 처리하는 메서드
    def discard_card(self, card: int) -> None:
        self.__discarded_card = cards.check_card(card)
        # 기술 카드 처리
        if self.__discarded_card.get("type") == "draw2":
            self.__force_draw += 2
        elif self.__discarded_card.get("type") == "reverse":
            if self.__reverse_direction is False:
                self.__reverse_direction = True
            else:
                self.__reverse_direction = False
        elif self.__discarded_card.get("type") == "skip":
            self.__skip_turn = True
        elif self.__discarded_card.get("color") == "wild":
            self.__players[self.__current_turn].choose_color(self)
            if self.__discarded_card.get("type") == "draw4":
                self.__force_draw += 4
            if self.__discarded_card.get("type") == "shuffle":
                for i in range(0, len(self.__players)):
                    shuffle_pile = []
                    shuffle_pile += self.__players[i].get_hand_cards()
                    self.__players[i].set_cards([])
                random.shuffle(shuffle_pile)
                while len(shuffle_pile) == 0:
                    self.__players[
                        (self.__current_turn + 1) % len(self.__players)
                    ].get_cards([shuffle_pile.pop(0)])

        self.__next_turn()
        return None

    # 우승자(즉, 손에 카드가 없는 플레이어)가 있는지 확인하는 메서드
    def check_winner(self) -> None:
        if len(self.__players[self.__current_turn].get_hand_cards()) == 0:
            self.__end_round()
        return None

    # 라운드 종료 후 점수를 계산하는 메서드
    def __end_round(self) -> None:
        points = 0
        for i in range(0, len(self.__players)):
            if i != self.__current_turn:
                points += self.__calc_points(
                    self.__players[self.__current_turn].get_hand_cards()
                )
        self.__players[self.__current_turn].add_points(points)
        return None

    # cards_list에 있는 카드들의 점수를 계산하는 메서드
    def __calc_points(self, cards_list: Iterable[int]) -> int:
        points = 0
        for card in cards_list:
            card_info = cards.check_card(card)
            if card_info.get("number") <= 9:
                points += card_info.get("number")
            elif card_info.get("number") <= 12:
                points += 20
            elif card_info.get("number") <= 14:
                points += 50
            elif card_info.get("number") <= 16:
                points += 40
        return points

    # player가 우노를 외칠 수 있는 상황인지 확인하고 처리하는 메서드
    def check_uno(self, player: Player | Bot) -> None:
        if (
            len(player.get_hand_cards()) == 2
            and len(player.get_discardable_cards_index()) >= 1
        ):
            pass
        else:
            self.draw_cards(3, player)
        return None

    # Game 객체 내의 플레이어 배열을 반환하는 메서드
    def get_players(self) -> List[Player | Bot]:
        return self.__players

    # 플레이어가 턴 종료 시 호출하는 메서드
    def end_turn(self) -> None:
        while self.__player_drawed is False:
            self.__players[self.__current_turn].draw_cards(1)
        self.__next_turn()
        return None

    # 다음 턴의 플레이어를 계산하는 메서드
    def __next_turn(self) -> None:
        self.__player_drawed = False

        # 스킵 및 방향 확인해 턴 넘기기
        if self.__skip_turn is False:
            if self.__reverse_direction is False:
                self.__current_turn = (self.__current_turn + 1) % len(self.__players)
            else:
                self.__current_turn = (self.__current_turn - 1) % len(self.__players)
        else:
            if self.__reverse_direction is False:
                self.__current_turn = (self.__current_turn + 2) % len(self.__players)
            else:
                self.__current_turn = (self.__current_turn - 2) % len(self.__players)
        return None

    # Game 객체 내의 모든 타이머를 활성화하는 메서드
    def start_timer(self) -> None:
        self.__turn_timer.start()
        self.__round_timer.start()
        return None

    # Game 객체 내의 모든 타이머를 일시정지하는 메서드
    def pause_timer(self) -> None:
        self.__turn_timer.pause()
        self.__round_timer.pause()
        return None

    # Game 객체 내의 모든 일시정지된 타이머를 재개하는 메서드
    def resume_timer(self) -> None:
        self.__turn_timer.resume()
        self.__round_timer.resume()
        return None

    def set_color(self, color: int | str) -> None:
        if color == 1 or color == "blue":
            self.__discarded_card.update(color="blue")
            pass
        elif color == 2 or color == "green":
            self.__discarded_card.update(color="green")
            pass
        elif color == 3 or color == "red":
            self.__discarded_card.update(color="red")
            pass
        elif color == 4 or color == "yellow":
            self.__discarded_card.update(color="yellow")
            pass
        else:
            raise ValueError("Invalid Color")
        return None
