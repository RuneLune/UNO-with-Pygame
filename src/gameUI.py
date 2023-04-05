import pygame
import colors
import events

from cards import Cards
from game import Game
from settings_function import Settings


class Game_UI:
    def __init__(self, settings):
        self.game = Game(6)  # 임시 플레이어 수
        self.cards = Cards(settings)
        self.settings = settings
        self.pause = False
        # load user and bot object
        self.players = self.game.get_players()
        self.bots = []

        # discrete user and computer
        for player in self.players:
            if player.get_name() == "Player":  # 이름 변경에따른 코드 수정 필요
                self.user = player
            else:
                self.bots.append(player)

        self.cards.refresh()
        self.card_size = self.cards.get_card_image(000).get_rect().size
        self.card_back_image = self.cards.get_card_image(000)
        self.card_color = (0, 150, 100)

        self.title_font = pygame.font.Font(None, 60)
        self.menu_font = pygame.font.Font(None, 40)
        self.mouse_pos = pygame.mouse.get_pos()

        # 타이머 스타트
        self.game.start_timer()

        self.refresh(6)  # 임시 플레이어 수

    def render(self):
        # each space's size,position definition
        deck_space_size = (self.screen_size[0] * (3 / 4), self.screen_size[1] * (2 / 3))
        deck_space_pos = (0, 0)

        user_space_size = (self.screen_size[0] * (3 / 4), self.screen_size[1] * (1 / 3))
        self.user_space_pos = (0, self.screen_size[1] * (2 / 3))

        self.bots_space_size = (
            self.screen_size[0] * (1 / 4),
            self.screen_size[1] * (1 / 5),
        )
        self.bots_space_pos = [
            (user_space_size[0], i * self.bots_space_size[1])
            for i in range(len(self.players))
        ]

        # space rectangular definition
        self.deck_space = pygame.Rect(deck_space_pos, deck_space_size)
        self.user_space = pygame.Rect(self.user_space_pos, user_space_size)
        self.bots_space = [
            pygame.Rect(self.bots_space_pos[i], self.bots_space_size)
            for i in range(len(self.players))
        ]

        # font for user, bot name
        self.font = pygame.font.Font("res/font/Travel.ttf", 20)
        self.user_name_text = self.font.render("insert_User_name", True, colors.white)
        self.bot_name_text = [
            self.font.render("computer " + str(i), True, colors.white)
            for i in range(len(self.bots))
        ]

        # user space 중앙 좌표
        self.user_card_center_pos = (
            self.user_space.centerx - self.card_size[0] / 2,
            self.user_space.centery - self.card_size[1] / 2,
        )
        
        # user card rendering
        self.user_card_list = self.user.get_hand_cards()
        self.user_card_num = len(self.user_card_list)
        self.user_card_image = [
            self.cards.get_card_image(num) for num in self.user_card_list
        ]
        self.user_card_pos = [
            (
                self.user_card_center_pos[0]
                + self.card_size[0] * (i - self.user_card_num // 2),
                self.user_card_center_pos[1]
            )
            for i in range(self.user_card_num)
        ]
        self.user_card_rect = [self.user_card_image[i].get_rect(
                                x=self.user_card_pos[i][0],
                                y=self.user_card_pos[i][1]+5
                                ) for i in range(self.user_card_num)]
        self.user_card_hover = [False for i in range(self.user_card_num)]
        
        # bot card position render
        self.bot_card_center_pos = [
            (
                self.bots_space[i].centerx - self.card_size[0] / 2,
                self.bots_space[i].centery - self.card_size[1] / 2,
            )
            for i in range(len(self.bots))
        ]

    def refresh(self, player_count):
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
        self.render()

    def draw(self):
        if self.pause is False:
            self.__draw_game()
            pass
        else:
            self.__draw_pause_menu()
            pass
        pass

    def __draw_game(self):
        self.screen.fill(colors.black)
        self.screen.blit(self.surface, (0, 0))

        # draw spaces and text
        pygame.draw.rect(self.surface, (0, 150, 100), rect=self.deck_space)
        pygame.draw.rect(self.surface, colors.white, rect=self.user_space, width=2)
        self.screen.blit(self.user_name_text, self.user_space_pos)

        for i in range(len(self.bots)):
            pygame.draw.rect(self.surface, colors.red, self.bots_space[i], width=2)
            self.screen.blit(self.bot_name_text[i], self.bots_space_pos[i])

        # 플레이어의 카드 그리기
        for i in range(self.user_card_num):
            self.screen.blit(self.user_card_image[i], self.user_card_pos[i])
            if self.user_card_hover[i] is True:
                pygame.draw.rect(self.surface, colors.red,
                                 self.user_card_rect[i], width=10)
            else:
                pygame.draw.rect(self.surface, colors.black,
                                 self.user_card_rect[i], width=10)

        # 봇의 카드그리기
        for i in range(len(self.bots)):
            bot_card_num = len(self.bots[i].get_hand_cards())
            for j in range(bot_card_num):
                self.screen.blit(
                    self.card_back_image,
                    (
                        self.bot_card_center_pos[i][0]
                        + self.card_size[0] * (j - bot_card_num / 2) // 2,
                        self.bot_card_center_pos[i][1],
                    ),
                )

    def __draw_pause_menu(self):
        title_text = self.title_font.render("Pause Menu", True, (255, 255, 255))
        continue_text = self.menu_font.render("Continue", True, (255, 255, 255))
        settings_text = self.menu_font.render("Settings", True, (255, 255, 255))
        start_menu_text = self.menu_font.render("Start Menu", True, (255, 255, 255))
        exit_text = self.menu_font.render("Exit", True, (255, 255, 255))

        # Get the size of the screen
        screen_width, screen_height = self.screen.get_size()

        # Set the position of the menu options
        title_pos = (self.screen.get_width() // 2 - title_text.get_width() // 2, 50)
        continue_pos = (
            screen_width // 2 - continue_text.get_width() // 2,
            screen_height // 2 - 75,
        )
        settings_pos = (
            screen_width // 2 - settings_text.get_width() // 2,
            screen_height // 2 - 25,
        )
        start_menu_pos = (
            screen_width // 2 - start_menu_text.get_width() // 2,
            screen_height // 2 + 25,
        )
        exit_pos = (
            screen_width // 2 - exit_text.get_width() // 2,
            screen_height // 2 + 75,
        )

        # Draw the menu options on the screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, title_pos)
        self.screen.blit(continue_text, continue_pos)
        self.screen.blit(settings_text, settings_pos)
        self.screen.blit(start_menu_text, start_menu_pos)
        self.screen.blit(exit_text, exit_pos)

        # # 정지 메뉴 이벤트
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if continue_text.get_rect(center=continue_pos).collidepoint(self.mouse_pos):
        #             # Code to resume the game
        #             pass
        #         elif settings_text.get_rect(center=settings_pos).collidepoint(self.mouse_pos):
        #             # Code to open the settings menu
        #             pass
        #         elif start_menu_text.get_rect(center=start_menu_pos).collidepoint(self.mouse_pos):
        #             # Code to go back to the start menu
        #             pass
        #         elif exit_text.get_rect(center=exit_pos).collidepoint(self.mouse_pos):
        #             pygame.quit()
        #             sys.exit()

    def get_pause(self):
        return self.pause

    def set_pause(self, pause):
        # 일시정지일 때
        if pause:
            self.pause = False
        # 일시정지 아닐 때
        else:
            self.pause = True

    def handle(self, event):
        if self.pause is False:
            self.__handle_game(event)
            pass
        else:  # self.pause is True
            self.__handle_pause_menu(event)
            pass
        pass

    def __handle_game(self, event):
        # 인게임 이벤트 처리(일시정지 버튼 포함)
        # 일시정지 버튼 클릭하면(또는 Esc 누르면)
        # 1. self.pause를 True로
        # 2. 모든 타이머 정지(self.game.pause_timer())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_pause(self.pause)
                self.game.pause_timer()
                self.settings.get_real_settings().update(previous_scene="gameui")
                return pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="settings")
                )
        for i in range(self.user_card_num):
            card = self.user_card_rect[i]
            if card.collidepoint(pygame.mouse.get_pos()):
                self.user_card_hover[i] = True
            else:
                self.user_card_hover[i] = False

    def __handle_pause_menu(self, event):
        # 일시정지 메뉴 이벤트 처리
        # 계속하기 버튼 클릭하면
        # 1. self.pause를 False로
        # 2. 모든 타이머 시작(self.game.resume_timer())
        # Check if any of the menu options are hovered over
        self.set_pause(self.pause)
        self.game.resume_timer()
