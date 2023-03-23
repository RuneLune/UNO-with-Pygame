import random
import copy

import cards


class Deck:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.draw_pile = (
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
        random.shuffle(self.draw_pile)
        self.discard_pile = self.draw_pile[:1]
        self.draw_pile = self.draw_pile[1:]
        self.discarded_info = cards.check_card(self.discard_pile[0])

        return super().__init__()

    def shuffle(self):
        discarded_cards = self.discard_pile[1:]
        random.shuffle(discarded_cards)
        self.draw_pile += discarded_cards
        self.discard_pile = self.discard_pile[:1]
        return self

    def draw_cards(self, count):
        if count >= len(self.draw_pile):
            self.shuffle()
        drawing_cards = copy.deepcopy(self.draw_pile[:count])
        self.draw_pile = self.draw_pile[count:]
        return drawing_cards

    # def discard(self, card):
    #     self.discarded_info = cards.check_card(card)


# class Bot:
#     def __new__(cls):
#         return super().__new__(cls)

#     def __init__(self):
#         self.cards = []
#         return super().__init__()

#     def draw(self, deck, count):
#         self.cards += deck.draw(count)
#         return len(self.cards)

#     def play_card(self, deck):
#         playable_cards =


class Player:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, game, name):
        self.__game = game
        self.__name = name
        self.__cards = []
        self.__turn = False
        self.__yelled_uno = False
        return super().__init__()

    def draw_cards(self, deck, count):
        self.__cards += self.__deck.draw_cards(count)
        self.__cards.sort()
        return len(self.__cards)

    def get_name(self):
        return self.__name

    def is_uno(self):
        return self.__yelled_uno

    def get_hand_cards(self):
        return copy.deepcopy(self.__cards)

    def turn_start(self):
        self.__turn = True

    def turn_end(self):
        self.__turn = False
        self.__game.next_turn()

    def discard_card(self, index, deck):
        deck.discard(self.__cards[index])
        del self.__cards[index]


class Game:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):

        self.running = True  # 게임 실행

        self.players = []  # 게임에 참여하는 players 리스트

        # 인간 플레이어 추가...

        # 봇 플레이어 추가...

        self.turn = -1  # players 리스트의 인덱스를 턴 넘버로 사용
        self.reverse = False  # 턴 방향

        return super().__init__()

    def turn(self):  # 턴
        if not self.reverse:  # 정방향
            self.turn += 1  # 그 다음 사람 턴
            if self.turn >= len(self.players):  # 턴 넘버가 리스트 인덱스 넘어간다면
                self.turn = 0  # 다시 첫 번째 player로 턴 변경
        else:  # 역방향
            self.turn -= 1  # 역방향이므로 그 전 사람 턴
            if self.turn < 0:  # 턴 넘버가 음수 된다면
                self.turn = len(self.players) - 1  # 제일 마지막 player로 턴 변경

    def whoisFirst(self):  # 플레이어 순서 정하기
        random.shuffle(self.players)  # players 순서 섞기
        return self.players[0]  # 첫 번째 플레이어 반환
    
class Hand:

    def __init__(self):
        self.hand = []
    
    # 패에 카드 넣기
    def add_card(self, card):
        self.hand.append(card)
    
    # 가지고 있는 카드 나타내기
    def has_card(self):
        return self.hand
    
    # 패에서 카드 내기
    def play_card(self, card_index):
        card = self.hand[card_index]
        del self.hand[card_index]
        return card
    
    # 패에서 카드 개수 확인
    def count(self):
        return len(self.hand)
    
    # 낼 수 있는 카드 확인
    def get_playable_cards(self, top_card):
        playable_cards = []
        for card in self.hand:
            if card.color == top_card.color or card.number == top_card.number or card.color == "wild":
                playable_cards.append(card)
            
        return playable_cards
