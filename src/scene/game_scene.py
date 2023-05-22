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
from gameobj.ingame.card_num_txt import CardNumber

from gameobj.txtobj import TextObject

from metaclass.singleton import SingletonMeta
from manager.gamemgr import GameManager
from manager.acvmgr import AchieveManager


# - 턴 스킵 표시
# - 일시정지 화면 o
# - 효과음 추가
# - 셔플 카드 오류 수정 o
# - 업적 달성 체크 o
# - 업적 달성 메세지 표현 o
# - 턴 종료시 자동 드로우 체크
# - 유저, 봇 이름 표시 o
# - 봇 카드 개수 표시 o
class GameScene(Scene):
    @overrides
    def start(self) -> None:
        self.game = GameManager().get_game()
        self.settings = Config()
        self.cards_cls = Cards()

        self.cards_cls.refresh()
        self.card_size = self.cards_cls.get_card_image(000).get_rect().size
        self.card_back_image = self.cards_cls.get_card_image(000)

        self.screen_size = self.settings.get_screen_resolution()
        self.user = self.game.get_user()
        self.user.set_cards([14, 14, 14])
        self.bots = self.game.get_bots()
        self.bots[0].set_cards([15, 15, 15, 15, 15])

        color_dict = [colors.red, colors.green, colors.blue, colors.yellow]

        # 업적 체크용 flag
        self.turn_count = 0
        self.no_tech = True
        self.speed_game = True
        self.same_card_count = 0
        self.same_card_code = 0
        self.same_card3 = False
        self.all_red = False

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
        self.deck_card.observer_update(self.game)

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
                if j >= 6:
                    temp = BotCard(
                        surface=self.card_back_image,
                        name=f"bot{i} card",
                        left=self.bot_card_pos_x[6],
                        top=self.bot_card_pos_y[i],
                        target_pos=self.discard_pile_pos,
                    )
                    self.bot_cards[i].append(temp)
                    continue
                temp = BotCard(
                    surface=self.card_back_image,
                    name=f"bot{i} card",
                    left=self.bot_card_pos_x[j],
                    top=self.bot_card_pos_y[i],
                    target_pos=self.discard_pile_pos,
                )
                self.bot_cards[i].append(temp)

        # 봇 카드 숫자 표시 오브젝트 생성
        self.bot_card_num = []
        for i, bot in enumerate(self.bots):
            temp = CardNumber(
                text=str(len(bot.get_hand_cards())),
                font=pygame.font.Font(
                    font_resource("MainFont.ttf"), round(self.bot_spaces[i].width / 5)
                ),
                color=colors.white,
                left=self.bot_card_pos_x[6] + self.card_size[0],
                top=self.bot_spaces[i].centery,
                z_index=1,
            )
            temp.observer_update(bot)
            self.bot_card_num.append(temp)
            self.instantiate(self.bot_card_num[i])

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

        self.key_input = KeyInput().attach_selector(self.selector)

        self.key_input.attach_card(
            self.user_cards_obj, self.deck_card, self.uno_btn, self.color_set
        )
        self.key_input.observer_update(self.game)
        self.instantiate(self.selector)
        self.instantiate(self.key_input)

        # 텍스트 오브젝트 생성
        self.winner_text = WinnerText(
            text="winner!",
            font=pygame.font.Font(font_resource("MainFont.ttf"), 100),
            color=colors.gold,
            width=self.screen_size[0] * 3 / 4,
            height=self.screen_size[1] * 1 / 5,
            z_index=1,
        )
        self.winner_text._visible = False

        self.firework1 = TextObject(
            text="(b˙◁˙ )b",
            font=pygame.font.Font(font_resource("MainFont.ttf"), 100),
            width=self.screen_size[0],
            height=self.screen_size[1] * 2 / 5,
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
            z_index=1,
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
            z_index=1,
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

        if self.user_space.time_left <= 5:
            self.speed_game = False

        # 승리조건 확인
        winner = self.game.check_winner()
        if winner is not None:
            if winner == self.user:
                self.achive_check(0)
                if self.game._name == "stage_D":
                    self.achive_check(1)
                if self.no_tech is True:
                    self.achive_check(3)
                if self.speed_game is True:
                    self.achive_check(5)
                for bot in self.bots:
                    if bot.is_uno() is True:
                        self.achive_check(4)
                        break
            elif winner == self.user and self.turn_count < 10:
                self.achive_check(2)

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
            # time.sleep(0.2)
            return None

        # 현재 턴 플레이어 표시
        if self.user.is_turn() is True:
            self.turn_count += 1

        # 카드 뽑기
        if self.deck_card.draw_flag is True or (
            self.user.is_turn() is True and self.game.remain_turn_time() < 0.1
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

        elif self.last_card.shuffle is True:
            self.last_card.shuffle = False
            self.user_cards_list = self.user.get_hand_cards()
            for obj in self.user_cards_obj:
                self.destroy(obj)
            self.user_cards_obj.clear()
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
            if diff == 0:
                continue
            elif diff > 0:
                last_index = len(self.bots[i].get_hand_cards()) - 1
                if last_index >= 6:
                    last_index = 6
                for j in range(0, diff):
                    # 카드 생성
                    if 6 - j < diff:
                        temp = BotCard(
                            surface=self.card_back_image,
                            name=f"bot{i} card",
                            left=self.draw_pile_pos[0],
                            top=self.draw_pile_pos[1],
                            target_pos=(
                                self.bot_card_pos_x[last_index],
                                self.bot_card_pos_y[i],
                            ),
                        )
                    else:
                        temp = BotCard(
                            surface=self.card_back_image,
                            name=f"bot{i} card",
                            left=self.draw_pile_pos[0],
                            top=self.draw_pile_pos[1],
                            target_pos=(
                                self.bot_card_pos_x[last_index - diff + j],
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
                # 업적 체크 G: 연속 3번 같은 숫자 내기
                if self.same_card3 is False:
                    if self.same_card_code == card.code:
                        self.same_card_count += 1
                        if self.same_card_count >= 2:
                            self.same_card3 = True
                            self.achive_check(6)
                    else:
                        self.same_card_code = card.code
                        self.same_card_count = 0

                if self.no_tech is True and card.code % 100 >= 10:
                    self.no_tech = False

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

        # 업적체크 H: 패에 한가지 색상 카드 모두 모으기
        if self.all_red is False:
            count = 0
            for i, card in enumerate(self.user_cards_obj):
                if i > 0:
                    if self.user_cards_obj[i - 1].code // 100 != card.code // 100:
                        count = 0
                    else:
                        count += 1
                if count == 9:
                    self.all_red = True
                    self.achive_check(7)

        self.key_input.attach_card(
            self.user_cards_obj, self.deck_card, self.uno_btn, self.color_set
        )

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
            diff.append(after - before)
        return diff

    def achive_check(self, idx):
        AchieveManager().update_achieve_state(idx)
        self.achive_rect.achive_text_update(idx)
        self.achive_rect.move_fwd = True
