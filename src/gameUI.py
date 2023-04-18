import pygame
from overrides import overrides
from typing import Dict, Type
import copy

import colors
import events
from cards import Cards
from game import Game
from settings_function import Settings
from sound import SoundManager
from resource_manager import image_resource, font_resource
from scene import Scene


class Game_UI(Scene):
    @overrides
    def __init__(self, settings: Settings, sound_manager: SoundManager):
        self.game: Type[Game] = Game(2)  # 임시 플레이어 수
        self.cards = Cards(settings)
        self.sounds = sound_manager
        self.settings = settings
        self.pause = False
        # load user and bot object
        self.players = self.game.get_players()
        self.bots = []
        self.user_card_pos = []
        self.discard_flag = False
        self.draw_flag = False
        self.winner_flag = False
        self.winner_name = "undefined"

        # discrete user and computer
        self.user = self.game.get_user()
        self.bots = self.game.get_bots()
        # for player in self.players:
        #     if player.get_name() == "Player":  # 이름 변경에따른 코드 수정 필요
        #         self.user = player
        #     else:
        #         self.bots.append(player)

        self.cards.refresh()
        self.card_size = self.cards.get_card_image(000).get_rect().size
        self.card_back_image = self.cards.get_card_image(000)
        self.card_color = (0, 150, 100)
        self.turn_img = pygame.image.load(image_resource("myturn.png"))
        self.draw_img = pygame.image.load(image_resource("draw.png"))
        self.current_color_dict = {
            "wild": colors.black,
            "red": colors.red,
            "blue": colors.blue,
            "green": colors.green,
            "yellow": colors.yellow,
            "black": colors.black,
        }
        self.color_list = [
            colors.blue,
            colors.green,
            colors.red,
            colors.yellow,
        ]
        self.color_choice = False

        self.title_font = pygame.font.Font(None, 60)
        self.menu_font = pygame.font.Font(None, 40)
        self.mouse_pos = pygame.mouse.get_pos()

        # 타이머 스타트
        self.game.start_timer()

        self.refresh()
        self.render()
        self.card_render()
        self.time_start_pos = self.user_space_pos
        self.time_end_pos = [self.user_space_size[0] / 10, self.deck_space_size[1]]

        return None

    # @overrides
    def get_args(self, args: Dict[any, any]) -> None:
        if "game" in args:
            self.game: Type[Game] = args.get("game")
            self.players = self.game.get_players()
            self.user = self.game.get_user()
            self.bots = self.game.get_bots()
            pass

        return None

    @overrides
    def render(self):
        if self.settings.get_settings().get("colorblind_mode") is False:
            self.current_color_dict = {
                "wild": colors.black,
                "red": colors.red,
                "blue": colors.blue,
                "green": colors.green,
                "yellow": colors.yellow,
                "black": colors.black,
            }
            self.color_list = [
                colors.blue,
                colors.green,
                colors.red,
                colors.yellow,
            ]
            pass
        else:
            self.current_color_dict = {
                "wild": colors.black,
                "red": colors.orange,
                "blue": colors.blue,
                "green": colors.colorblinemode_green,
                "yellow": colors.yellow,
                "black": colors.black,
            }
            self.color_list = [
                colors.blue,
                colors.colorblinemode_green,
                colors.orange,
                colors.yellow,
            ]
            pass

        # each space's size,position definition
        self.deck_space_size = (
            self.screen_size[0] * (3 / 4),
            self.screen_size[1] * (2 / 3),
        )
        deck_space_pos = (0, 0)

        self.user_space_size = (
            self.screen_size[0] * (3 / 4),
            self.screen_size[1] * (1 / 3),
        )
        self.user_space_pos = (0, self.screen_size[1] * (2 / 3))

        self.bots_space_size = (
            self.screen_size[0] * (1 / 4),
            self.screen_size[1] * (1 / 5),
        )
        self.bots_space_pos = [
            (self.user_space_size[0], i * self.bots_space_size[1])
            for i in range(len(self.players))
        ]

        # space rectangular definition
        self.deck_space = pygame.Rect(deck_space_pos, self.deck_space_size)
        self.user_space = pygame.Rect(self.user_space_pos, self.user_space_size)
        self.bots_space = [
            pygame.Rect(self.bots_space_pos[i], self.bots_space_size)
            for i in range(len(self.players))
        ]

        # font for user, bot name
        self.font = pygame.font.Font(font_resource("MainFont.ttf"), 25)
        self.user_name_text = self.font.render(self.user.get_name(), True, colors.white)
        self.bot_name_text = [
            self.font.render(bot.get_name(), True, colors.white) for bot in self.bots
        ]
        self.font2 = pygame.font.Font(font_resource("MainFont.ttf"), 15)

        # 우승자 이름 렌더링
        self.winner_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(self.screen_size[1] / 10)
        )
        self.winner_text1 = self.winner_font.render("You", True, colors.gold)
        self.winner_text2 = self.winner_font.render(" Are", True, colors.gold)
        self.winner_text3 = self.winner_font.render("  Winner", True, colors.gold)
        self.winner_text5 = self.winner_font.render(
            "click to main menu", True, colors.gold
        )

        # bot card position render
        self.bot_card_first_pos = [
            (
                self.bots_space[i].x + 10,
                self.bots_space[i].centery - self.card_size[1] / 2,
            )
            for i in range(len(self.bots))
        ]

        # uno 버튼 렌더링
        uno_img = pygame.image.load(image_resource("uno.png"))
        self.uno_btn = pygame.transform.scale_by(uno_img, 0.1)
        self.uno_btn_gray = pygame.transform.grayscale(self.uno_btn)
        self.uno_btn_size = self.uno_btn.get_rect().size
        self.uno_btn_pos = (
            self.deck_space_size[0] - self.uno_btn_size[0] - 10,
            self.deck_space_size[1] - self.uno_btn_size[1] - 10,
        )
        self.uno_btn_rect = self.uno_btn.get_rect(
            x=self.uno_btn_pos[0], y=self.uno_btn_pos[1]
        )
        self.bot_uno_btn_img = self.uno_btn
        self.bot_uno_btn_pos = [
            (
                self.user_space_size[0]
                + self.bots_space_size[0] / 2
                - self.uno_btn_size[0] / 2,
                self.bots_space_size[1] * i + 15,
            )
            for i in range(len(self.bots))
        ]
        self.uno_btn_hover = False

        # 색깔 표시 rect 렌더링
        self.color_rect_size = (30, 30)
        self.color_rect_pos = (self.deck_space.centerx, self.deck_space.centery)
        self.color_rect = pygame.Rect(self.color_rect_pos, self.color_rect_size)

        self.choice_rect_size = self.color_rect_size
        self.choice_rect_pos = [
            (
                self.deck_space.centerx + self.card_size[0] * 2 + self.card_size[0],
                self.deck_space.centery - self.color_rect_size[1] / 2 - 90 + 60 * i,
            )
            for i in range(4)
        ]
        self.choice_rect = [
            pygame.Rect(self.choice_rect_pos[i], self.choice_rect_size)
            for i in range(4)
        ]
        self.choice_rect_hover = [False for i in range(4)]

        # 현재 색깔 불러오기
        self.discard_card = self.game.get_discard_info().get("discarded_card")
        self.current_color = self.discard_card.get("color")

        # 턴 표시 화살표 벡터 렌더링
        self.p1 = pygame.Vector2(
            self.deck_space.centerx,
            self.deck_space.centery - self.card_size[1] * 1.5 - 40 - 5,
        )
        self.p2 = pygame.Vector2(
            self.deck_space.centerx + 40,
            self.deck_space.centery - self.card_size[1] * 1.5 - 5,
        )
        self.p3 = pygame.Vector2(
            self.deck_space.centerx,
            self.deck_space.centery - self.card_size[1] * 1.5 + 40 - 5,
        )

        # 턴 알림 이미지 렌더링
        self.turn_tran_size = [
            self.deck_space.size[0] / 3,
            self.deck_space.size[1] / 3,
        ]
        self.turn_img_tran = pygame.transform.scale(self.turn_img, self.turn_tran_size)
        self.turn_img_size = self.turn_img_tran.get_rect().size
        self.turn_img_pos = [
            self.user_space_pos[0] - self.turn_img_size[0],
            self.user_space_pos[1] - self.turn_img_size[1],
        ]

    @overrides
    def refresh(self):
        pygame.display.set_caption("Game")
        # if full screen
        flag = 0
        if self.settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN

        # screen definition
        self.screen_size = self.settings.get_screen_resolution()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.surface = pygame.Surface(self.screen_size)

        self.players = self.game.get_players()
        self.cards.refresh()
        self.card_size = self.cards.get_card_image(000).get_rect().size
        self.card_back_image = self.cards.get_card_image(000)
        self.render()
        self.card_render()
        self.time_start_pos = self.user_space_pos
        self.time_end_pos = [self.user_space_size[0] / 10, self.deck_space_size[1]]

    @overrides
    def draw(self):
        if self.pause is False:
            self.__draw_game()
            pass
        else:
            self.sounds.stop_background_sound()
            pass
        pass

    def __draw_game(self):
        self.game.tick()
        # self.tick()
        self.screen.fill(colors.black)
        self.screen.blit(self.surface, (0, 0))

        # draw spaces and text
        pygame.draw.rect(self.surface, (0, 150, 100), rect=self.deck_space)
        pygame.draw.rect(
            self.surface, self.turn_color(self.user), rect=self.user_space, width=2
        )
        self.screen.blit(self.user_name_text, self.user_space_pos)

        for i in range(len(self.bots)):
            pygame.draw.rect(
                self.surface, self.turn_color(self.bots[i]), self.bots_space[i], width=2
            )
            self.screen.blit(self.bot_name_text[i], self.bots_space_pos[i])

        # 카드 내기 애니메이션
        if self.discard_flag is True:
            self.screen.blit(self.discard_card_img, self.discard_pos)

        # 카드 뽑기 애니메이션
        if self.draw_flag is True:
            for i in range(len(self.draw_card)):
                if self.draw_flag_list[i] is True:
                    self.screen.blit(self.draw_card[i], self.draw_pos[i])

        # 플레이어의 카드 그리기
        if self.user_card_num == 1:
            self.screen.blit(self.user_card_image[0], self.user_card_pos)
        else:
            for i in range(self.user_card_num):
                self.screen.blit(self.user_card_image[i], self.user_card_pos[i])
                if self.user_card_hover[i] is True:
                    pygame.draw.rect(self.surface, colors.red, self.user_card_rect[i])
                else:
                    pygame.draw.rect(self.surface, colors.black, self.user_card_rect[i])

        # 봇의 카드그리기
        for i in range(len(self.bots)):
            bot_card_num = len(self.bots[i].get_hand_cards())
            if bot_card_num == 0:
                x = self.bot_card_first_pos[i][0]
                y = self.bot_card_first_pos[i][1]
            for j in range(bot_card_num):
                if j > 5:
                    break
                x = self.bot_card_first_pos[i][0] + j * self.card_size[0] * 1 / 2
                y = self.bot_card_first_pos[i][1]
                self.screen.blit(self.card_back_image, (x, y))
            card_num_text = self.font2.render(
                "total cards: " + str(bot_card_num), True, colors.white
            )
            self.screen.blit(
                card_num_text,
                (self.bot_card_first_pos[i][0] + 70, self.bots_space_pos[i][1] + 5),
            )

        # 드로우카드 더미 하이라이팅
        if self.draw_pile_hover is True:
            pygame.draw.rect(self.surface, colors.red, self.draw_pile_rect, width=10)

        # 드로우카드,버린카드 더미 그리기
        discard_code = self.game._discard_pile[0]
        self.discard = self.cards.get_card_image(discard_code)
        self.screen.blit(self.card_back_image, self.draw_pile_pos)
        self.screen.blit(self.discard, self.discard_pile_pos)

        # uno버튼 그리기
        if self.uno_btn_hover is True:
            self.screen.blit(self.uno_btn, self.uno_btn_pos)
        else:
            self.screen.blit(self.uno_btn_gray, self.uno_btn_pos)

        for i in range(len(self.bots)):
            if self.bots[i].is_uno() is True:
                self.screen.blit(self.bot_uno_btn_img, self.bot_uno_btn_pos[i])

        # 턴 시작시 알림
        if self.user.is_turn() is True:
            self.screen.blit(self.turn_img_tran, self.turn_img_pos)

        # 드로우 권장 알림
        if (
            self.user.is_turn() is True
            and self.color_choice is False
            and len(self.user.get_discardable_cards_index()) == 0
        ):
            self.screen.blit(self.draw_img_tran, self.draw_img_pos)

        # 색깔표시 rect 그리기
        pygame.draw.circle(
            self.surface,
            color=self.current_color_dict[self.current_color],
            center=self.deck_space.center,
            radius=self.card_size[0] * 2.5,
            width=25,
        )

        # 색 변경 버튼 그리기
        if self.color_choice is True and self.user.is_turn() is True:
            for i in range(0, 4):
                pygame.draw.rect(
                    self.surface,
                    color=self.color_list[i],
                    rect=self.choice_rect[i],
                    border_radius=5,
                )

        # 턴 진행방향 표시 화살표 그리기
        if self.user.is_turn() is False:
            pygame.draw.polygon(
                self.surface,
                color=self.current_color_dict[self.current_color],
                points=[self.p1, self.p2, self.p3],
            )
            pygame.draw.line(
                self.surface,
                color=(0, 150, 100),
                start_pos=self.p1,
                end_pos=self.p2,
                width=5,
            )
            pygame.draw.line(
                self.surface,
                color=(0, 150, 100),
                start_pos=self.p2,
                end_pos=self.p3,
                width=5,
            )

        # 턴 남은 시간 그리기
        time = self.game.remain_turn_time()
        if self.user.is_turn() is True:
            pygame.draw.line(
                self.surface,
                color=colors.yellow,
                start_pos=self.time_start_pos,
                end_pos=(self.time_end_pos[0] * time, self.time_end_pos[1]),
                width=10,
            )
        else:
            pygame.draw.line(
                self.surface,
                color=colors.yellow,
                start_pos=self.time_start_pos,
                end_pos=(self.time_end_pos[0] * 10, self.time_end_pos[1]),
                width=10,
            )

        # 승리 텍스트 표시
        if self.winner_flag is True:
            self.screen.blit(
                self.winner_text1,
                (self.screen_size[0] / 8, 1 * self.screen_size[1] / 8),
            )
            self.screen.blit(
                self.winner_text2,
                (self.screen_size[0] / 8, 2 * self.screen_size[1] / 8),
            )
            self.screen.blit(
                self.winner_text3,
                (self.screen_size[0] / 8, 3 * self.screen_size[1] / 8),
            )
            self.screen.blit(
                self.winner_text4,
                (self.screen_size[0] / 2, self.screen_size[1] / 4),
            )
            self.screen.blit(
                self.winner_text5,
                (self.screen_size[0] / 8, 7 * self.screen_size[1] / 8),
            )

        self.tick()

    def get_pause(self):
        return self.pause

    def set_pause(self, pause):
        # 일시정지일 때
        if pause:
            self.pause = False
        # 일시정지 아닐 때
        else:
            self.pause = True

    def tick(self):
        # 턴 알림 이미지 위치 조정
        if self.user.is_turn() is True:
            if self.turn_img_pos[0] < 0:
                self.turn_img_pos[0] += self.turn_img_size[0] / 60
            else:
                self.turn_img_pos[0] = 0
        else:
            self.turn_img_pos[0] = self.user_space_pos[0] - self.turn_img_size[0]

        # hover 체크
        self.draw_pile_hover = self.hover_check(self.draw_pile_rect)
        if self.user.is_uno() is False:
            self.uno_btn_hover = self.hover_check(self.uno_btn_rect)
        if self.user_card_num == 1:
            self.user_card_hover[0] = self.hover_check(self.user_card_rect)
        else:
            for i, rect in enumerate(self.user_card_rect):
                self.user_card_hover[i] = self.hover_check(rect)

        # 카드 내기 애니메이션 위치 계산
        if self.discard_flag is True:
            if (
                self.discard_pos[0] < self.discard_end[0]
                and self.discard_pos[1] > self.discard_end[1]
            ) or (
                self.discard_pos[0] > self.discard_end[0]
                and self.discard_pos[1] > self.discard_end[1]
            ):
                self.discard_pos[0] += self.discard_rate_x
                self.discard_pos[1] += self.discard_rate_y
            else:
                self.discard_flag = False

        # 카드 뽑기 애니메이션 위치 계산
        if self.draw_flag is True:
            for i in range(len(self.draw_card)):
                if self.draw_flag_list[i] is True:
                    if (
                        self.draw_pos[i][0] > self.draw_end[i][0]
                        and self.draw_pos[i][1] < self.draw_end[i][1]
                    ) or (
                        self.draw_pos[i][0] < self.draw_end[i][0]
                        and self.draw_pos[i][1] < self.draw_end[i][1]
                    ):
                        self.draw_pos[i][0] += self.draw_rate_x[i]
                        self.draw_pos[i][1] += self.draw_rate_y[i]
                    else:
                        self.draw_flag_list[i] = False
                        self.draw_flag_list[i + 1] = True
        # if self.draw_flag is True:
        #     if self.draw_counter < 10 * len(self.draw_card):
        #         idx = self.draw_counter // 10
        #         self.draw_pos[idx][0] += self.draw_rate_x[idx]
        #         self.draw_pos[idx][1] += self.draw_rate_y[idx]
        #         self.draw_counter += 1
        #         if self.draw_counter % 10 == 0:
        #             self.draw_flag_list[idx] = False
        #             self.draw_flag_list[idx + 1] = True
        #             pass
        #         pass
        #     else:
        #         self.draw_flag = False
        #         self.draw_counter = 0
        #         pass
        #     pass

        # 현재 컬러 확인
        self.discard_card = self.game.get_discard_info().get("discarded_card")
        self.current_color = self.discard_card.get("color")

        # 턴 종료시 하이라이팅 비활성화
        if self.user.is_turn() is False:
            self.user_card_hover = [False for i in range(len(self.user_card_rect))]

        # 진행방향 체크
        if self.game._reverse_direction is True:
            self.p2 = pygame.Vector2(
                self.deck_space.centerx - 40,
                self.deck_space.centery - self.card_size[1] * 1.5 - 5,
            )
        else:
            self.p2 = pygame.Vector2(
                self.deck_space.centerx + 40,
                self.deck_space.centery - self.card_size[1] * 1.5 - 5,
            )

        # 드로우 권장 이미지 렌더링, 코드 위치 변경 필요
        self.draw_tran_size = [
            self.deck_space.size[0] / 5,
            self.deck_space.size[1] / 5,
        ]
        self.draw_img_tran = pygame.transform.scale(self.draw_img, self.draw_tran_size)
        self.draw_img_size = self.turn_img_tran.get_rect().size
        self.draw_img_pos = [
            self.draw_pile_pos[0] - self.draw_img_size[0] / 6,
            self.draw_pile_pos[1] - self.draw_img_size[1] / 3,
        ]

    @overrides
    def handle(self, event):
        if self.pause is False:
            self.sounds.play_background_sound()
            self.__handle_game(event)
            pass
        else:  # self.pause is True
            self.sounds.stop_background_sound()
            self.__handle_pause_menu(event)
            pass
        pass

    def __handle_game(self, event):
        # 인게임 이벤트 처리(일시정지 버튼 포함)
        # 일시정지 버튼 클릭하면(또는 Esc 누르면)
        # 1. self.pause를 True로
        # 2. 모든 타이머 정지(self.game.pause_timer())

        self.card_render()
        self.card_lift()
        self.tick()

        # 게임 종료시 마우스 입력 받고 메인메뉴로 이동
        if self.game._game_status is False:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="main")
                )

        # 턴 시간초과시
        if event.type == events.TURN_TIMEOUT:
            self.color_choice = False
            self.sounds.play_effect("timeout")
            pass

        # 일시정지 화면전환 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_pause(self.pause)
                self.game.pause_timer()
                self.settings.previous_gameui()
                self.winner_flag = False
                return pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="settings")
                )

        # 승자 이름 가져오기
        if event.type == events.GAME_END:
            if hasattr(event, "args") and "winner" in event.args:
                self.winner_name = event.args.get("winner")
                self.winner_text4 = self.winner_font.render(
                    self.winner_name + "!", True, colors.gold
                )
                self.winner_flag = True

        if event.type == events.BOT_DRAW:
            pass

        if event.type == events.BOT_DISCARD:
            pass

        # 카드 내기 처리
        index_list = self.user.get_discardable_cards_index()
        if index_list:
            for index in index_list:
                if self.user_card_hover[index] and event.type == pygame.MOUSEBUTTONDOWN:
                    self.sounds.play_effect("discard")
                    self.ani_discard(index, self.user_card_list[index])
                    self.user.discard_card(index)
                    self.user_card_hover[index] = False

        # 카드 뽑기 처리
        if (
            self.draw_pile_hover is True
            and event.type == pygame.MOUSEBUTTONDOWN
            and self.color_choice is False
            and self.user.is_turn() is True
        ):
            self.sounds.play_effect("draw")
            self.user.draw_cards()
            self.ani_draw()

        # 색깔 고르기 처리
        if event.type == events.ASK_COLOR:
            self.color_choice = True
            self.draw_flag = False

        for i, rect in enumerate(self.choice_rect):
            self.choice_rect_hover[i] = self.hover_check(rect)
            if (
                self.choice_rect_hover[i] is True
                and event.type == pygame.MOUSEBUTTONDOWN
            ):
                self.user.set_color(i + 1)
                self.color_choice = False

        # uno 버튼 클릭 이벤트 진행
        if self.uno_btn_hover is True and event.type == pygame.MOUSEBUTTONDOWN:
            self.user.yell_uno()

    def __handle_pause_menu(self, event):
        self.set_pause(self.pause)
        self.game.resume_timer()

    def card_render(self):
        # user card 처음 좌표
        self.user_card_first_pos = [
            self.user_space.x + self.card_size[0] // 2,
            self.user_space.centery - self.card_size[1] // 2,
        ]

        # user card rendering
        self.user_card_list = self.user.get_hand_cards()
        self.user_card_num = len(self.user_card_list)
        self.user_card_image = [
            self.cards.get_card_image(num) for num in self.user_card_list
        ]
        self.user_card_pos = [
            [
                self.user_card_first_pos[0] + i * self.card_size[0] * 4 / 5,
                self.user_card_first_pos[1],
            ]
            for i in range(0, self.user_card_num + 4)
        ]

        # 유저 카드 rect 렌더링
        if self.user_card_num == 1:
            self.user_card_pos = self.user_card_first_pos
            self.user_card_rect = self.user_card_image[0].get_rect(
                x=self.user_card_pos[0], y=self.user_card_pos[1] + 5
            )
        else:
            self.user_card_rect = [
                self.user_card_image[i].get_rect(
                    x=self.user_card_pos[i][0], y=self.user_card_pos[i][1] + 5
                )
                for i in range(self.user_card_num)
            ]
        self.user_card_hover = [False for i in range(self.user_card_num)]

        # draw pile and discard pile render
        self.draw_pile_pos = (
            self.deck_space.centerx - self.card_size[0] * 1.5,
            self.deck_space.centery - self.card_size[1] / 2,
        )
        self.draw_pile = pygame.Rect(self.draw_pile_pos, self.card_size)
        self.draw_pile_rect = self.card_back_image.get_rect(
            x=self.draw_pile_pos[0], y=self.draw_pile_pos[1] + 5
        )
        self.draw_pile_hover = False

        # 최근에 버린 카드 정보 불러오기
        self.discard_color = self.game.get_discard_info().get("color")
        self.discard_code = self.game._discard_pile[0]
        self.discard = self.cards.get_card_image(self.discard_code)

        # 버린카드 위치
        self.discard_pile_pos = (
            self.deck_space.centerx + self.card_size[0] / 2,
            self.deck_space.centery - self.card_size[1] / 2,
        )
        self.discard_pile = pygame.Rect(self.discard_pile_pos, self.card_size)

    # 마우스 충돌 확인 함수
    def hover_check(self, rect):
        if rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    # 낼 수 있는 카드 위치 변경 함수
    def card_lift(self):
        if self.user.is_turn() is True and self.user_card_num <= 1:
            pass
        elif self.user.is_turn() is True:
            for index in self.user.get_discardable_cards_index():
                self.user_card_pos[index][1] -= 10
        else:
            self.user_card_pos[:][1] = self.user_card_first_pos[1]

    # 해당 턴이면 빨강색 반환
    def turn_color(self, player):
        if player.is_turn() is True:
            return colors.red
        else:
            return colors.white

    def ani_discard(self, index, card):
        self.discard_flag = True
        self.discard_card_img = self.cards.get_card_image(card)

        if self.user_card_num == 1:
            self.discard_start = self.user_card_pos
        else:
            self.discard_start = self.user_card_pos[index]
        self.discard_end = self.discard_pile_pos
        self.discard_pos = self.discard_start  # initial pos

        self.discard_rate_x = (self.discard_end[0] - self.discard_start[0]) / 10
        self.discard_rate_y = (self.discard_end[1] - self.discard_start[1]) / 10

    def ani_draw(self):
        self.draw_flag = True
        # self.draw_counter = 0
        self.last_draw_card = self.user.get_last_drawing_cards()
        print(self.last_draw_card)
        self.draw_flag_list = []
        self.draw_card = []
        self.draw_end = []
        self.draw_rate_x = []
        self.draw_rate_y = []
        self.draw_pos = []
        self.draw_start = [self.draw_pile_pos[0], self.draw_pile_pos[1]]

        for i, index in enumerate(self.last_draw_card):
            if i == 0:
                self.draw_flag_list.append(True)
            else:
                self.draw_flag_list.append(False)
            self.draw_card.append(self.cards.get_card_image(index[1]))
            if self.user_card_num == 1:
                self.draw_end.append(self.user_card_pos)
            else:
                self.draw_end.append(self.user_card_pos[index[0]])
            self.draw_rate_x.append((self.draw_end[i][0] - self.draw_start[0]) / 10)
            self.draw_rate_y.append((self.draw_end[i][1] - self.draw_start[1]) / 10)
            self.draw_pos.append(copy.deepcopy(self.draw_start))  # initial pos

        self.draw_flag_list.append(False)
