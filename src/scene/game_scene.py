from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene

from game.game import Game
from manager.cfgmgr import Config
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
        self.game = Game(6)
        self.settings = Config()
        self.cards_cls = Cards()

        self.cards_cls.refresh()
        self.card_size = self.cards_cls.get_card_image(000).get_rect().size
        self.card_back_image = self.cards_cls.get_card_image(000)

        self.screen_size = self.settings.get_screen_resolution()
        self.user = self.game.get_user()
        self.bots = self.game.get_bots()

        self.iter = 0

        # space 정의
        self.user_space = Space(
            surface=pygame.Surface((0, 0)),
            name="user_space",
            width=self.screen_size[0] * (3 / 4),
            height=self.screen_size[1] * (1 / 3),
            left=0,
            top=self.screen_size[1] * (2 / 3),
        )

        self.bot_spaces = [
            Space(
                surface=pygame.Surface((0, 0)),
                name=f"bot{i}_space",
                width=self.screen_size[0] * (1 / 4),
                height=self.screen_size[1] * (1 / 5),
                left=self.screen_size[0] * (3 / 4),
                top=self.screen_size[1] * (1 / 5) * i,
            )
            for i in range(len(self.bots))
        ]

        self.deck_space = Space(
            surface=pygame.Surface((0, 0)),
            name="deck_space",
            width=self.screen_size[0] * (3 / 4),
            height=self.screen_size[1] * (2 / 3),
            left=0,
            top=0,
            color=color.alice_blue,
        )

        # 드로우 파일 카드 위치 정의
        self.draw_pile_pos = (
            self.screen_size[0] * (3 / 8) - self.card_size[0],
            self.screen_size[1] * (1 / 3) - self.card_size[1] / 2,
        )
        self.deck_card = Deck(
            surface=self.cards_cls.get_card_image(000),
            name="000",
            width=self.card_size[0],
            height=self.card_size[1],
            left=self.draw_pile_pos[0],
            top=self.draw_pile_pos[1],
        )

        # 버린 카드 위치 정의
        self.discard_pile_pos = (
            self.screen_size[0] * 3 / 8 + self.card_size[0],
            self.screen_size[1] * 1 / 3 - self.card_size[1] / 2,
        )

        # 버린 카드 객체 로드
        self.last_card = LastCard(
            surface=self.cards_cls.get_card_image(self.game._discard_pile[0]),
            name="LastCard",
            left=self.discard_pile_pos[0],
            top=self.discard_pile_pos[1],
        )

        # 플레이어 카드 위치 정의
        self.user_card_pos = [
            (
                (i + 1) * self.card_size[0] * 3 / 4,
                self.screen_size[1] * (2 / 3) + self.card_size[1] / 2,
            )
            if i <= 14
            else (
                (i + 1) * self.card_size[0] * 3 / 4,
                self.screen_size[1] * (2 / 3) + self.card_size[1] * 3 / 2,
            )
            for i in range(40)
        ]

        # 처음 유저 카드 정의
        self.user_cards_list = self.user.get_hand_cards()
        self.user_cards = []
        for i, code in enumerate(self.user_cards_list):
            temp = Card(
                surface=self.cards_cls.get_card_image(code),
                name="user_card",
                width=self.card_size[0],
                height=self.card_size[1],
                left=self.user_card_pos[i][0],
                top=self.user_card_pos[i][1],
                target_pos=self.discard_pile_pos,
                code=code,
            )
            temp.user = True
            temp.observer_update(self.game)
            self.user_cards.append(temp)

        self.instantiate(self.deck_space)
        self.instantiate(self.user_space)
        for i in range(len(self.bots)):
            self.instantiate(self.bot_spaces[i])

        for i in range(len(self.user_cards)):
            self.instantiate(self.user_cards[i])

        self.instantiate(self.last_card)
        self.instantiate(self.deck_card)

    @overrides
    def update(self):
        self.game.tick()
        self.deck_card.observer_update(self.game)
        self.last_card.observer_update(self.game)
        self.turn_update(self.user_cards)

        # 현재 턴 플레이어 표시
        if self.user.is_turn() is True:
            self.user_space.turn = True
        else:
            self.user_space.turn = False
        for i, bot in enumerate(self.bots):
            if bot.is_turn() is True:
                self.bot_spaces[i].turn = True
            else:
                self.bot_spaces[i].turn = False

        # 카드 뽑기
        if self.deck_card.draw_flag is True or (
            self.user_cards_list != self.user.get_hand_cards()
        ):
            self.user_cards_list = self.user.get_hand_cards()
            self.user.draw_cards()
            drawing_cards = self.user.get_last_drawing_cards()
            # 뽑은 카드 생성 후 유저 공간으로 이동
            for i, tuple in enumerate(drawing_cards):
                idx = tuple[0]
                code = tuple[1]
                temp = Card(
                    surface=self.cards_cls.get_card_image(code),
                    name=f"{code}",
                    width=self.card_size[0],
                    height=self.card_size[1],
                    left=self.draw_pile_pos[0],
                    top=self.draw_pile_pos[1],
                    target_pos=self.user_card_pos[idx],
                    code=code,
                )
                temp.user = True
                temp.draw_start = True
                self.user_cards.append(temp)
                self.instantiate(temp)

            self.deck_card.draw_flag = False

        # 카드 내기
        for i, card in enumerate(self.user_cards):
            if card.discard_start is True:
                self.user.discard_card(i)

        # 애니메이션 종료후 카드 위치 재정의
        for i, card in enumerate(self.user_cards):
            if card.discard_end is True:
                self.user_cards.remove(card)
                self.index_update(self.user_cards)
            if card.draw_end is True:
                self.index_update(self.user_cards)
                break

    def index_update(self, list):
        for i in range(len(list)):
            list[i].observer_update(self.game)

    def turn_update(self, list):
        for i in range(len(list)):
            list[i].turn_update(self.game)

    # self.user_cards_list = self.user.get_hand_cards()
