import random
import copy

import cards
from player import Player


class Game:
    # MAX_Inst = 1
    # Inst_created = 0

    def __new__(cls, *args, **kwargs):
        # if cls.Inst_created >= cls.MAX_Inst:
        #     raise ValueError("Cannot create more Game object")
        # cls.Inst_created += 1
        return super().__new__(cls)

    # 객체 초기화 함수
    def __init__(
        self,
        players_count,
        turn_seconds=10,
        round_seconds=-1,
        max_rounds=-1,
        target_score=500,
    ):
        # 봇 및 플레이어 추가
        self.__players = []
        for i in range(0, players_count - 1):
            self.__players.append(Player(self, "Player " + (i + 1)))
        self.__players.append(Player(self, "User"))
        random.shuffle(self.__players)

        self.__turn_seconds = turn_seconds
        self.__round_seconds = round_seconds
        self.__max_rounds = max_rounds
        self.__target_score = target_score

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
            + list(range(cards.wild_normal, cards.wild_draw + 1)) * 4
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
        self.__force_draw = 0
        self.__reverse_direction = False
        self.__current_turn = 1
        self.__skip_turn = False
        if self.__discarded_card.get("type", None) == "draw2":
            self.__force_draw = 2
        elif self.__discarded_card.get("type", None) == "reverse":
            self.__current_turn = 0
            self.__reverse_direction = True
        elif self.__discarded_card.get("type", None) == "skip":
            self.__current_turn = 2 % len(self.__players)
        # elif self.__discarded_card.get("color", None) == "wild":  # 미구현
        #     # self.__players[1].choose_color(self)

        self.__player_drawed = False

        return super().__init__()

    # 패산 셔플
    def __shuffle(self):
        discarded_cards = self.__discard_pile[1:]
        random.shuffle(discarded_cards)
        self.__draw_pile += discarded_cards
        self.__discard_pile = self.__discard_pile[:1]
        return self

    # 마지막으로 낸 카드 정보
    def get_discard_info(self):
        return {
            "force_draw": self.__force_draw,
            "discarded_card": copy.deepcopy(self.__discarded_card),
        }

    # 카드 드로우
    def draw_cards(self, count, player):
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
        # if len(drawing_cards) == 1:
        #     draw_card = cards.check_card(drawing_cards[0])
        #     if (
        #         draw_card.get("color") == "wild"
        #         or draw_card.get("color") == self.__discarded_card.get("color")
        #         or draw_card("number") == self.__discarded_card.get("number")
        #     ):
        #         self.__players[self.__current_turn].ask_discard()
        self.__force_draw = 0
        return len(drawing_cards)

    # 카드 내기
    def discard_card(self, card):
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
            # self.__players[self.__current_turn].choose_color(self)
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
        pass

    def check_winner(self):
        if len(self.__players[self.__current_turn].get_hand_cards()) == 0:
            self.__end_game()
        pass

    def __end_game(self):
        points = 0
        for i in range(0, len(self.__players)):
            if i != self.__current_turn:
                points += self.__calc_points(
                    self.__players[self.__current_turn].get_hand_cards()
                )
        self.__players[self.__current_turn].add_points(points)
        pass

    def __calc_points(self, cards_list):
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

    def check_uno(self, player):
        if (
            len(player.get_hand_cards()) == 2
            and len(player.get_discardable_cards_index()) >= 1
        ):
            pass
        else:
            self.draw_cards(3, player)
        pass

    def get_players(self):
        return self.__players

    # 턴 종료시 호출 함수
    def end_turn(self):
        while self.__player_drawed is False:
            self.__players[self.__current_turn].draw_cards(1)
        self.__next_turn()

    # 턴 넘기는 함수
    def __next_turn(self):
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

    # def set_color(self):
    #     return
