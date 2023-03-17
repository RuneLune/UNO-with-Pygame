import random

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

    def draw(self, count):
        if count >= len(self.draw_pile):
            self.shuffle()
        drawing_cards = self.draw_pile[:count]
        self.draw_pile = self.draw_pile[count:]
        return drawing_cards

    """def discard(self, card):
        self.discarded_info = cards.check_card(card)"""


class Bot:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.cards = []
        return super().__init__()

    def draw(self, deck, count):
        self.cards += deck.draw(count)
        return len(self.cards)

    """def play_card(self, deck):
        playable_cards = """

class Startgame:
    def __new__(cls):
        return super().__new__(cls)
    
    def __init__(self):
        return super().__init__()
    
    def order(self):
        return self