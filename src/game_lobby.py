import pygame
import colors
import events

from user import User
from bot import Bot
from cards import Cards
from game import Game


class Game_Lobby:
    def __init__(self, settings):
        # self.game = Game(6) # 임시 플레이어 수
        self.__settings = settings
        self.refresh()

        # load user and bot object
        # self.players = self.game.get_players()
        self.bots = []

        return super().__init__()
    
    def render(self):
        # 스크린 사이즈
        screen_size = self.__settings.get_screen_resolution()
        self.surface = pygame.Surface(screen_size)

        # 폰트 생성
        self.__game_font = pygame.font.Font("res/font/Travel.ttf", round(screen_size[1] / 15))
        self.__back_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 20))
        self.__start_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 10))

        # 덱/유저/봇 공간 사이즈와 위치 정의
        deck_space_size = (screen_size[0]*(3/4),screen_size[1]*(2/3))
        deck_space_pos = (0,0)

        user_space_size = (screen_size[0]*(3/4), screen_size[1]*(1/3))
        self.user_space_pos = (0,deck_space_size[1])
        
        self.bots_space_size = (screen_size[0]*(1/4), screen_size[1]*(1/5))
        self.bots_space_pos = [(user_space_size[0],i * self.bots_space_size[1]) for i in range(0,5)]

        # 공간 사각형 정의
        self.deck_space = pygame.Rect(deck_space_pos, deck_space_size)
        self.user_space = pygame.Rect(self.user_space_pos, user_space_size)
        self.bots_space = [pygame.Rect(self.bots_space_pos[i], self.bots_space_size) for i in range(0,5)]

        # self.user_name_text = self.font.render("insert_User_name", True, colors.white)
        # self.bot_name_text =[self.font.render("computer " + i, True, colors.white) for i in range(0,5)]

        # 뒤로가기 버튼 추가
        self.__button_text.append(self.__back_font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[-1].bottom = self.__screen.get_rect().centery / 5

        # 스타트 버튼 추가 및 스타트 버튼 위에 start 출력
        self.__button_text.append(self.__start_font.render("Start Game", True, colors.white))
        self.__button_rect.append(pygame.Rect(0,0,self.user_space.width * 2/3, self.user_space.height * 2/3))
        self.__button_rect[-1].centerx = self.user_space.centerx
        self.__button_rect[-1].centery = self.user_space.centery
        self.__start_surface = pygame.Surface((self.user_space.width * 2/3, self.user_space.height * 2/3))
        self.__start_surface.fill((196,216,214))
        self.__start_text_rect = self.__button_text[-1].get_rect(center=self.__start_surface.get_rect().center)
        self.__start_surface.blit(self.__button_text[-1], self.__start_text_rect)

        # 봇 이름 리스트 및 이름 공간 사각형 정의
        self.bot_names = ["Computer One", "Computer Two", "Computer Three", "Computer Four", "Computer Five"]
        self.bot_names_text = [self.__game_font.render(self.bot_names[i], True, colors.white) for i in range(len(self.bot_names))]
        self.bot_names_rects = [self.bot_names_text[i].get_rect(topleft=self.bots_space[i].topleft) for i in range(len(self.bot_names))]
        self.bot_name_inputs = [(self.bot_names_rects[i], self.bot_names_text[i]) for i in range(5)]

        # 봇 영역 버튼 리스트에 추가
        for i in range(len(self.bots_space)):
            self.__button_rect.append(self.bots_space[i])

    def refresh(self):
        pygame.display.set_caption("Game Lobby")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN        
        # 스크린 생성
        self.__screen = pygame.display.set_mode(self.__settings.get_screen_resolution(), flag)
        self.__button_text = []
        self.__button_rect = []
        self.render()
        return None

    def draw(self):
        # 스크린 채우기
        self.__screen.fill(colors.black)
        self.__screen.blit(self.surface, (0, 0))

        # 각 공간 그리기
        pygame.draw.rect(self.__screen, (50, 100, 80), self.deck_space)
        pygame.draw.rect(self.__screen, (80, 120, 80), self.user_space)
        pygame.draw.rect(self.__screen, colors.white, self.user_space, width=2)
        # 봇 영역 - 회색, 빨간색 테두리, 하얀색 봇 이름
        for i in range(len(self.bots_space)):
            pygame.draw.rect(self.__screen, (50, 50, 50), self.bots_space[i])
            pygame.draw.rect(self.__screen, colors.red, self.bots_space[i], width=2)
            self.__screen.blit(self.bot_names_text[i], self.__button_rect[i+2])

        # 스크린 위에 뒤로가기 버튼, 스타트 버튼 그리기
        self.__screen.blit(self.__button_text[0], self.__button_rect[0])
        self.__screen.blit(self.__start_surface, self.__button_rect[1])

        # 봇 이름 봇 영역 위에 출력하고 스크린에 바로 출력
        # for i in range(len(self.bot_names)):
        #     self.__bot_surface = pygame.Surface((self.bots_space_size))
        #     self.__bot_surface.fill((50,50,50))
        #     self.__bot_surface.blit(self.bot_names_text[i], self.bot_names_rects[i])
        #     self.__screen.blit(self.__bot_surface, self.__button_rect[i+2])

        return None

    # 봇 이름 수정을 위한 입력 박스 생성 함수
    def create_input_box(self, pos, size, text):
        input_box = pygame.Rect(pos, size)
        input_text = self.__game_font.render(text, True, colors.black)
        return input_box, input_text

            # # 봇 이름 수정 입력 박스 출력
            # if bot_name_inputs[i]:
            #     pygame.draw.rect(self.__screen, colors.white, bot_name_inputs[i][0])
            #     self.__screen.blit(bot_name_inputs[i][1], bot_name_inputs[i][0].topleft)

    # 봇 이름 수정 가능 입력 박스 출력하는 함수
    def draw_bot_names_modify(self, bot_name_inputs):
        if bot_name_inputs:
            pygame.draw.rect(self.__screen, colors.white, bot_name_inputs[0])
            self.__screen.blit(bot_name_inputs[1], bot_name_inputs[0].topleft)
    
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_rect)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    return self.__button_func(i)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="main")
                )
            # 봇 이름 수정
            # for i in range(len(self.bot_names_rects)):
            #     if self.bot_names_rects[i].collidepoint(mouse_pos):
            #         # 마우스 클릭시 봇 이름 수정 가능한 입력 박스 생성
            #         self.bot_name_inputs[i] = self.create_input_box(self.bots_space[i].topleft, self.bot_names_rects[0].size, self.bot_names[i])
            #     else:
            #         # 다른 곳을 클릭하면 입력 박스 삭제
            #         self.bot_name_inputs[i] = None

        return "continue"
    
    def __button_func(self, i):
        # 뒤로 가기 버튼
        if i == 0:
            self.__settings.previous_gamelobby()
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="main"))
        # 게임 시작 버튼
        elif i == 1:
            self.__settings.previous_gamelobby()
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="gameui"))
        # 봇 추가/삭제 버튼. 없을 때도 버튼이 활성화 되어 있음. 봇 1~5
        elif 1 < i < 7:
            print(f"clicked {i}")
            pass
        # 이름 수정 버튼
        else:
            # 이름 수정하는 함수 정의 필요
            pass

        return None
