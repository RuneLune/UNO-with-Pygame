from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene

from game.game import Game
from config.settings_function import Settings
from card.cards import Cards

from gameobj.gameobj import GameObject
from gameobj.ingame.card import Card
from gameobj.ingame.space import Space
from gameobj.ingame.deck import Deck
from gameobj.ingame.lastcard import LastCard

from metaclass.singleton import SingletonMeta


class GameScene(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.game = Game(2)
        self.settings = Settings()
        self.cards_cls = Cards(Settings)

        self.cards_cls.refresh()
        self.card_size = self.cards_cls.get_card_image(000).get_rect().size
        self.card_back_image = self.cards_cls.get_card_image(000)

        self.screen_size = self.settings.get_screen_resolution()
        self.user = self.game.get_user()
        self.bots = self.game.get_bots()

        # space 정의
        self.user_space = Space(
            name="user_space",
            width=self.screen_size[0] * 3 / 4,
            height=self.screen_size[1] * 1 / 3,
            left=0,
            top=self.screen_size[1] * 2 / 3,
            z_index=0,
        )
        self.instantiate(self.user_space)

        self.game.attach(self.user_space)
        self.bot_spaces = [
            Space(
                name="bot_space",
                width=self.screen_size[0] * 1 / 4,
                height=self.screen_size[1] * 1 / 5,
                left=self.screen_size[0] * 3 / 4,
                top=self.screen_size[1] * 1 / 5 * i,
                z_index=0,
            )
            for i in range(len(self.bots))
        ]
        for i in range(len(self.bots)):
            self.instantiate(self.bot_spaces[i])

        self.deck_space = Space(
            name="deck_space",
            width=self.screen_size[0] * 3 / 4,
            height=self.screen_size[1] * 2 / 3,
            left=0,
            top=0,
            z_index=0,
        )
        self.instantiate(self.deck_space)

        # 드로우 파일 카드 위치 정의
        self.draw_cards_pos = (
            self.screen_size[0] * 3 / 4 * 1 / 2 - self.card_size[0],
            self.screen_size[1] * 1 / 3 - self.card_size[1] / 2,
        )
        # 드로우 카드 객체 모두 로드
        self.draw_cards = []
        for i, code in enumerate(self.game._draw_pile):
            temp = Card(
                self.cards_cls.get_card_image(code),
                name=code,
                width=self.card_size[0],
                height=self.card_size[1],
                left=self.draw_cards_pos[0],
                top=self.draw_cards_pos[1],
                code=code,
            )
            temp._visible = False
            temp._active = False
            self.draw_cards.append(temp)

        for i in range(len(self.draw_cards)):
            self.instantiate(self.draw_cards[i])

        # 버린 카드 위치 정의
        self.discard_pile_pos = (
            self.screen_size[0] * 3 / 4 * 1 / 2 + self.card_size[0],
            self.screen_size[1] * 1 / 3 - self.card_size[1] / 2,
        )
        # 버린 카드 객체 로드
        self.last_cards = []
        self.last_cards.append(
            Card(
                self.cards_cls.get_card_image(self.game._discard_pile[0]),
                name=self.game._discard_pile[0],
                width=self.card_size[0],
                height=self.card_size[1],
                left=self.discard_pile_pos[0],
                top=self.discard_pile_pos[1],
                code=self.game._discard_pile[0],
            )
        )
        self.instantiate(self.last_cards[0])

        # 플레이어 카드 위치 정의
        self.user_card_pos = [
            (
                (i + 1) * self.card_size[0] / 3,
                self.screen_size[1] * (2 / 3) + self.card_size[1] / 2,
            )
            for i in range(100)
        ]

        # 처음 유저 카드 정의
        self.user_cards_list = self.user.get_hand_cards()
        self.user_cards = [
            Card(
                self.cards_cls.get_card_image(code),
                name="user_card",
                width=self.card_size[0],
                height=self.card_size[1],
                left=self.user_card_pos[i][0],
                top=self.user_card_pos[i][1],
                target_pos=self.discard_pile_pos,
                code=code,
            )
            for i, code in enumerate(self.user_cards_list)
        ]

        for i in range(len(self.user_cards)):
            self.instantiate(self.user_cards)

    @overrides
    def update(self):
        if self.user.is_turn():
            self.user_space.turn = True
        else:
            self.user_space.turn = False

        for i, bot in enumerate(self.bots):
            if bot.is_turn() is True:
                self.bot_spaces[i].turn = True
            else:
                self.bot_spaces[i].turn = False

        # self.user_cards_list = self.user.get_hand_cards()
