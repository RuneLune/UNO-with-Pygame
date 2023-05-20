from overrides import overrides
import pygame
import time

from util.resource_manager import font_resource
import util.colors as colors
from .scene import Scene

from game.game import Game
from manager.cfgmgr import Config
from manager.lobbymgr import LobbyManager
from card.cards import Cards

from gameobj.bgobj import BackgroundObject
from gameobj.gameobj import GameObject
from gameobj.ingame.card import Card
from gameobj.ingame.space import Space
from gameobj.ingame.deck_space import DeckSpace
from gameobj.ingame.deck import Deck
from gameobj.ingame.lastcard import LastCard
from gameobj.ingame.bot_card import BotCard
from gameobj.ingame.color_set import ColorSet
from gameobj.ingame.uno_btn import UnoBtn
from gameobj.ingame.key_input import KeyInput
from gameobj.ingame.selector import Selector
from gameobj.ingame.winner_txt import WinnerText
from gameobj.ingame.back_txt import BackToMain
from gameobj.ingame.achive_rect import AchiveRect

from gameobj.txtobj import TextObject

from metaclass.singleton import SingletonMeta


# - 턴 스킵 표시
# - 일시정지 화면 o
# - 효과음 추가
# - 셔플 카드 오류 수정
# - 업적 달성 체크
# - 업적 달성 메세지 표현 o
class GameScene(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.game = Game(LobbyManager().get_game_settings().get("player_count"))
        self.settings = Config()
        self.cards_cls = Cards()

        self.cards_cls.refresh()
        self.card_size = self.cards_cls.get_card_image(000).get_rect().size
        self.card_back_image = self.cards_cls.get_card_image(000)

        self.screen_size = self.settings.get_screen_resolution()
        self.user = self.game.get_user()
        self.user.set_cards([14, 15])
        # self.user._yelled_uno = True
        self.bots = self.game.get_bots()

        color_dict = [colors.red, colors.green, colors.blue, colors.yellow]

        # space 정의
        self.user_space = Space(
            surface=pygame.Surface((0, 0)),
            name="user_space",
            width=self.screen_size[0] * (3 / 4),
            height=self.screen_size[1] * (1 / 3),
            left=0,
            top=self.screen_size[1] * (2 / 3),
            player=self.user,
            game=self.game,
        )

        self.bot_spaces = [
            Space(
                surface=pygame.Surface((0, 0)),
                name=f"bot{i}_space",
                width=self.screen_size[0] * (1 / 4),
                height=self.screen_size[1] * (1 / 5),
                left=self.screen_size[0] * (3 / 4),
                top=self.screen_size[1] * (1 / 5) * i,
                player=bot,
                game=self.game,
            )
            for i, bot in enumerate(self.bots)
        ]

        self.deck_space = DeckSpace(
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
        self.bot_card_pos_x = [
            (self.bot_spaces[0].left + i * self.card_size[0] * 1 / 3)
            for i in range(0, 7)
        ]
        self.bot_card_pos_y = [
            (self.bot_spaces[i].top + self.bot_spaces[i].height / 5)
            for i in range(len(self.bots))
        ]

        # 봇 처음 카드 생성
        self.bot_cards = [[] for i in range(len(self.bots))]
        for i, bot in enumerate(self.bots):
            for j in range(len(bot.get_hand_cards())):
                temp = BotCard(
                    surface=self.card_back_image,
                    name=f"bot{i} card",
                    left=self.bot_card_pos_x[j],
                    top=self.bot_card_pos_y[i],
                    target_pos=self.discard_pile_pos,
                )
                self.bot_cards[i].append(temp)

        # 색 선택 오브젝트 생성
        self.color_set = []
        for i, color in enumerate(color_dict):
            temp = ColorSet(
                surface=pygame.Surface((0, 0)),
                name="choice_rect",
                width=self.card_size[0] * 2 / 3,
                height=self.card_size[0] * 2 / 3,
                left=self.discard_pile_pos[0] + self.card_size[0] * 2.5,
                top=self.discard_pile_pos[1]
                + (i - 1) * 1.5 * self.card_size[0] * 3 / 4,
                color=color,
            )
            self.color_set.append(temp)
            temp.user_update(self.game)
        # 우노 버튼 오브젝트 생성
        self.uno_btn = UnoBtn(
            surface=pygame.Surface((0, 0)),
            width=self.deck_space.width / 5,
            height=self.deck_space.width / 5 * 3 / 4,
        )
        self.uno_btn.left, self.uno_btn.top = (
            self.user_space.topright[0] - self.uno_btn.width,
            self.user_space.topright[1] - self.uno_btn.height,
        )
        self.uno_btn.observer_update(self.user)

        # 키보드 입력 오브젝트 생성
        self.selector = Selector()
        self.instantiate(self.selector)

        self.key_input = KeyInput().attach_selector(self.selector)
        self.instantiate(self.key_input)

        self.key_input.attach_card(
            self.user_cards_obj, self.deck_card, self.uno_btn, self.color_set
        )
        self.key_input.observer_update(self.game)

        # 텍스트 오브젝트 생성
        self.winner_text = WinnerText(
            text="winner!",
            font=pygame.font.Font(font_resource("MainFont.ttf"), 100),
            color=colors.gold,
            width=self.screen_size[0] * 3 / 4,
            height=self.screen_size[1] * 1 / 5,
        )
        self.winner_text._visible = False

        self.firework1 = TextObject(
            text="(b˙◁˙ )b",
            font=pygame.font.Font(font_resource("MainFont.ttf"), 100),
            width=self.screen_size[0],
            height=self.screen_size[1] * 2.5 / 5,
            top=self.winner_text.height,
            color=colors.light_salmon,
            z_index=1,
        )

        self.firework2 = TextObject(
            text="(o˙◁˙ )o",
            font=pygame.font.Font(font_resource("MainFont.ttf"), 100),
            width=self.screen_size[0],
            height=self.screen_size[1] * 2 / 5,
            top=self.winner_text.height,
            color=colors.light_salmon,
        )
        self.firework1._visible = False
        self.firework2._visible = False

        # 승리시 메인 화면 이동 텍스트 오브젝트 생성
        self.back_to_main = BackToMain(
            text="Back to Main",
            font=pygame.font.Font(font_resource("MainFont.ttf"), 100),
            color=colors.white,
            left=0,
            top=self.user_space.top,
        )
        self.back_to_main._visible = False
        self.back_to_main._enabled = False
        self.back_to_main.attach_mgr(self.scene_manager, "main_menu")

        # 업적 달성 표시 오브젝트 생성
        self.achive_rect = AchiveRect(
            pygame.Surface((0, 0)),
            width=self.screen_size[0] * 8 / 9,
            height=self.screen_size[1] * 1 / 11,
            left=self.screen_size[0] * 1 / 18,
            top=-self.screen_size[1] * 1 / 8,
            z_index=1,
        )
        self.achive_rect.move_fwd = True

        # 오브젝트 등록
        self.instantiate(BackgroundObject(colors.black))
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
        for i in range(4):
            self.instantiate(self.color_set[i])
            self.color_set[i].user_update(self.game)
        self.instantiate(self.uno_btn)
        self.instantiate(self.winner_text)
        self.instantiate(self.back_to_main)
        self.instantiate(self.firework1)
        self.instantiate(self.firework2)
        self.instantiate(self.achive_rect)

    @overrides
    def update(self):
        if self.key_input.pause is True:
            self.key_input.pause = False
            self.game.pause_timer()
            self.scene_manager.load_scene("config_menu")
        else:
            self.game.resume_timer()
            self._update()

    def _update(self):
        self.game.tick()
        self.deck_card.observer_update(self.game)
        self.last_card.observer_update(self.game)
        self.deck_space.observer_update(self.game)
        self.turn_update(self.user_cards_obj)
        self.key_input.state_update()
        for i in range(4):
            self.color_set[i].observer_update(self.game)

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
        if self.deck_card.draw_flag is True:
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
        elif self.last_card.shuffle is True:
            self.last_card.shuffle = False
            self.user_cards_list = self.user.get_hand_cards()
            for obj in self.user_cards_obj:
                self.destroy(obj)
            self.user_cards_obj = []

            # 뽑은 카드 생성 후 유저 공간으로 이동
            for i, code in enumerate(self.user_cards_list):
                temp = Card(
                    surface=self.cards_cls.get_card_image(code),
                    name=f"{code}",
                    width=self.card_size[0],
                    height=self.card_size[1],
                    left=self.draw_pile_pos[0],
                    top=self.draw_pile_pos[1],
                    target_pos=self.user_card_pos[i],
                    code=code,
                    index=i,
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
            last_index = len(self.bots[i].get_hand_cards()) - 1
            if last_index >= 6:
                last_index = 6
            if diff == 0:
                continue
            elif diff > 0:
                for j in range(diff, 0, -1):
                    # 카드 생성
                    temp = BotCard(
                        surface=self.card_back_image,
                        name=f"bot{i} card",
                        left=self.draw_pile_pos[0],
                        top=self.draw_pile_pos[1],
                        target_pos=(
                            self.bot_card_pos_x[last_index - j + 1],
                            self.bot_card_pos_y[i],
                        ),
                    )
                    self.instantiate(temp)
                    temp.draw_start = True
                    self.bot_cards[i].append(temp)
            elif diff < 0:
                # 카드 삭제
                for j in range(
                    len(self.bot_cards[i]) - 1,
                    len(self.bot_cards[i]) - 1 - abs(diff),
                    -1,
                ):
                    card = self.bot_cards[i][j]
                    card.discard_start = True
                    card.observer_update(self.game)
                    self.bot_cards[i].remove(card)

        # 카드 내기
        for i, card in enumerate(self.user_cards_obj):
            if card.discard_start is True:
                self.user.discard_card(i)
                self.user_cards_list = self.user.get_hand_cards()

        # 애니메이션 종료후 카드 위치 재정의
        # user card
        for i, card in enumerate(self.user_cards_obj):
            if card.discard_end is True:
                self.user_cards_obj.remove(card)
                self.destroy(card)
                self.position_update(self.user_cards_obj)
                break
            if card.draw_end is True:
                self.position_update(self.user_cards_obj)
                card.draw_end = False
                break
        # bot card
        for i, cards in enumerate(self.bot_cards):
            for j, card in enumerate(cards):
                if card.discard_end is True:
                    self.bot_cards[i].remove(card)
                    self.destroy(card)
                    break
                if card.draw_end is True:
                    card.draw_end = False
                    break

        # 키 입력 받는 오브젝트 업데이트
        self.key_input.attach_card(
            self.user_cards_obj, self.deck_card, self.uno_btn, self.color_set
        )

        # 승리조건 확인
        winner = self.game.check_winner()
        if winner is not None:
            self.winner_text.render(f"{winner.get_name()} is winner!")
            self.winner_text._visible = True
            self.back_to_main._enabled = True
            self.back_to_main._visible = True
            if self.firework1._visible is True:
                self.firework1._visible = False
                self.firework2._visible = True
            else:
                self.firework1._visible = True
                self.firework2._visible = False
            time.sleep(0.2)

    def position_update(self, obj_list: list):
        obj_list.sort(key=lambda x: x.code)
        for idx, obj in enumerate(obj_list):
            obj.position_update(self.game, idx)

    def turn_update(self, list):
        for i in range(len(list)):
            list[i].turn_update(self.game)

    def bot_card_difference(self, bots: list):
        diff = []
        for i, bot in enumerate(bots):
            before = len(self.bot_cards[i])
            after = len(bot.get_hand_cards())
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
