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
from gameobj.ingame.bot_card import BotCard
from gameobj.ingame.color_display import ColorDisplay

from metaclass.singleton import SingletonMeta


# -봇 처음 카드 생성 o
# -봇 카드수 업데이트 o
#   -봇 카드 뽑기 및 내기 애니메이션
# -턴 스킵 표시
# -턴 남은 시간 표시
# -현재 색깔 표시 o
# -유저 턴 표시 이미지
# -뽑을 카드 없을 시 드로우 권장 표시
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
            color=(0, 150, 100),
        )
        self.deck_space.deck = True

        # 드로우 파일 카드 위치 정의
        self.draw_pile_pos = (
            self.screen_size[0] * (3 / 8) - self.card_size[0] + 1,
            self.screen_size[1] * (1 / 3) - self.card_size[1] / 2 + 1,
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
            self.screen_size[0] * 3 / 8 + self.card_size[0] + 1,
            self.screen_size[1] * 1 / 3 - self.card_size[1] / 2 + 1,
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
                (i + 1) * self.card_size[0],
                self.screen_size[1] * (2 / 3) + self.card_size[1] / 2,
            )
            if i < 10
            else (
                (i - 9) * self.card_size[0],
                self.screen_size[1] * (2 / 3) + self.card_size[1] * 3 / 2,
            )
            for i in range(30)
        ]

        # 처음 유저 카드 정의
        self.user_cards_list = self.user.get_hand_cards()
        self.user_cards_obj = []
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
                index=i,
            )
            temp.user = True
            temp.position_update(self.game, i)
            self.user_cards_obj.append(temp)

        # 봇 카드 위치 정의
        self.bot_card_pos = [
            (
                self.bot_spaces[i].left,
                self.bot_spaces[i].top + self.bot_spaces[i].height / 5,
            )
            for i, bot in enumerate(self.bots)
        ]

        # 봇 처음 카드 생성
        self.bot_cards = [[] for i in range(len(self.bots))]
        for i, bot in enumerate(self.bots):
            for j in range(len(bot.get_hand_cards())):
                temp = BotCard(
                    surface=self.card_back_image,
                    name=f"bot{i} card",
                    left=self.bot_card_pos[i][0] + j * self.card_size[0] * 1 / 3,
                    top=self.bot_card_pos[i][1],
                    target_pos=self.discard_pile_pos,
                )
                self.bot_cards[i].append(temp)

        # 색깔 표시 오브젝트 생성
        self.color_display = ColorDisplay(
            surface=pygame.surface,
            name="color_display",
            width=self.screen_size[1] / 2,
            height=self.screen_size[1] / 2,
            left=self.deck_space.centerx - self.screen_size[1] / 2,
            top=self.deck_space.centery - self.screen_size[1] / 2,
        )

        # 오브젝트 등록
        self.instantiate(self.deck_space)
        self.instantiate(self.user_space)
        for i in range(len(self.bots)):
            self.instantiate(self.bot_spaces[i])
            for j in range(len(self.bot_cards[i])):
                self.instantiate(self.bot_cards[i][j])

        for i in range(len(self.user_cards_obj)):
            self.instantiate(self.user_cards_obj[i])

        self.instantiate(self.last_card)
        self.instantiate(self.deck_card)
        self.instantiate(self.color_display)

    @overrides
    def update(self):
        self.game.tick()
        self.deck_card.observer_update(self.game)
        self.last_card.observer_update(self.game)
        self.color_display.observer_update(self.game)
        self.turn_update(self.user_cards_obj)

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

        # 카드 더미를 눌러서 카드 뽑기
        if self.deck_card.draw_flag is True or (
            self.deck_card.draw_flag is False
            and (self.user_cards_list != self.user.get_hand_cards())
        ):
            self.user.draw_cards()
            drawing_cards = self.user.get_last_drawing_cards()
            self.user_cards_list = self.user.get_hand_cards()

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
                    index=idx,
                )
                self.instantiate(temp)
                temp.user = True
                temp.draw_start = True
                self.user_cards_obj.append(temp)
            self.turn_update(self.user_cards_obj)
            self.deck_card.draw_flag = False

        # last card가 셔플인 경우
        # 수정필요
        if self.last_card.code == 15 and (
            self.user_cards_list != self.user.get_hand_cards()
        ):
            self.user_cards_list = self.user.get_hand_cards()
            print(self.user_cards_list)
            for obj in self.user_cards_obj:
                self.destroy(obj)
            self.user_cards_obj = []
            drawing_cards = self.user.get_last_drawing_cards()
            print(drawing_cards)

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
                    index=idx,
                )
                self.instantiate(temp)
                temp.user = True
                temp.draw_start = True
                self.user_cards_obj.append(temp)
            self.turn_update(self.user_cards_obj)

        # 마지막 카드가 턴 스킵 카드인 경우

        # 봇 카드 개수 업데이트
        diff_list = self.bot_card_difference(self.bots)
        for i, diff in enumerate(diff_list):
            if diff == 0:
                pass
            elif diff > 0:
                for j in range(diff):
                    # 카드 생성
                    temp = BotCard(
                        surface=self.card_back_image,
                        name=f"bot{i} card",
                        left=self.draw_pile_pos[0],
                        top=self.draw_pile_pos[1],
                        target_pos=self.bot_card_pos[i],
                    )
                    self.instantiate(temp)
                    temp.draw_start = True
                    self.bot_cards[i].append(temp)
            elif diff < 0:
                for j in range(abs(diff)):
                    card = self.bot_cards[i][-j - 1]
                    self.bot_cards[i].remove(card)
                    card.discard_start = True
                    # 카드 삭제
                    pass

        # 카드 내기
        for i, card in enumerate(self.user_cards_obj):
            if card.discard_start is True:
                self.user.discard_card(i)
                self.user_cards_list = self.user.get_hand_cards()

        # 애니메이션 종료후 카드 위치 재정의
        for i, card in enumerate(self.user_cards_obj):
            if card.discard_end is True:
                self.user_cards_obj.remove(card)
                self.destroy(card)
                self.position_update(self.user_cards_obj)
                print(self.user_cards_list)
            if card.draw_end is True:
                self.position_update(self.user_cards_obj)
                card.draw_end = False

    def position_update(self, obj_list: list):
        obj_list.sort(key=lambda x: x.code)
        for idx, obj in enumerate(obj_list):
            obj.position_update(self.game, idx)

    def turn_update(self, list):
        for i in range(len(list)):
            list[i].turn_update(self.game)

    def bot_card_difference(self, bots: list):
        for i, bot in enumerate(bots):
            before = len(self.bot_cards[i])
            after = len(bot.get_hand_cards())
            diff = []
            if before == after:
                diff.append(0)
            elif before >= 7 and after >= 7:
                diff.append(0)
            elif before >= 7 and after < 7:  # 카드 삭제
                diff.append(after - before)
            elif before < 7 and after >= 7:  # 카드 생성 7개까지
                diff.append(7 - before)
            elif before < 7 and after < 7:
                diff.append(after - before)
        return diff
