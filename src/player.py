import copy

import cards


class Player:
    def __new__(cls, *args, **kwargs):
        return super(Player, cls).__new__(cls)

    def __init__(self, game, name):
        self.__game = game
        self.__name = name
        self.__cards = []
        self.__turn = False
        self.__yelled_uno = False
        self.__points = 0
        return super(Player, self).__init__()

    def draw_cards(self, count):
        self.__game.draw_cards(count,self)
        return len(self.__cards)

    def get_cards(self, cards_list):
        self.__cards += cards_list
        self.__cards.sort()
        return len(cards_list)

    def set_cards(self, cards_list):
        self.__cards = copy.deepcopy(cards_list)
        return len(self.__cards)

    def get_name(self):
        return self.__name

    def is_uno(self):
        return self.__yelled_uno

    def get_hand_cards(self):
        return copy.deepcopy(self.__cards)

    def turn_start(self):
        self.__turn = True
        self.__check_discardable_cards()

    def turn_end(self):
        self.__turn = False
        self.__game.next_turn()

    def add_points(self, points):
        self.__points += points
        return self.__points

    def get_points(self):
        return self.__points

    # 낼 수 있는 카드 확인
    def __check_discardable_cards(self):
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

    def get_discardable_cards_index(self):
        return copy.deepcopy(self.__discardable_cards_index)

    def discard_card(self, index):
        self.__game.discard_card(self.__cards[index])
        del self.__cards[index]

    def end_turn(self):
        self.__game.end_turn()

    # def choose_color(self):
    #     self.__game.set_color()

    # def ask_discard(self):
