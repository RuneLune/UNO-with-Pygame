import pygame
import colors
import events

from user import User
from bot import Bot
from cards import Cards
from game import Game


class Game_Lobby:
    def __init__(self, settings):
        self.user = User()
        self.bot = Bot()
        self.__settings = settings
        self.refresh()

        return super().__init__()
    
    def render(self):
        # 스크린 사이즈
        screen_size = self.__settings.get_screen_resolution()

        # 폰트 생성
        self.font = pygame.font.Font("res/font/Travel.ttf", round(screen_size[1] / 15))

        # 덱/유저/봇 공간 사이즈와 위치 정의
        deck_space_size = (screen_size[0]*(2/3),screen_size[1]*(3/5))
        deck_space_pos = (0,0)

        user_space_size = (screen_size[0]*(2/3), screen_size[1]*(2/5))
        self.user_space_pos = (0,screen_size[1]*(2/5))
        
        bots_space_size = (screen_size[0]*(1/3), screen_size[1]*(1/5))
        self.bots_space_pos = [(user_space_size[0],i * bots_space_size[1]) for i in range(0,5)]

        # 공간 사각형 정의
        self.deck_space = pygame.Rect(deck_space_pos, deck_space_size)
        self.user_space = pygame.Rect(self.user_space_pos, user_space_size)
        self.bots_space = [pygame.Rect(self.bots_space_pos[i], bots_space_size) for i in range(0,5)]

        # 봇 이름 리스트 및 이름 공간 사각형 정의
        self.bot_names = ["Computer1", "Computer2", "Computer3", "Computer4", "Computer5"]
        self.bot_names_rects = [self.bot_names[i].get_rect() for i in range(len(self.bot_names))]
        self.bot_name_inputs = [(self.bot_names_rects[i], self.bot_names[i]) for i in range(5)]

        # self.user_name_text = self.font.render("insert_User_name", True, colors.white)
        # self.bot_name_text =[self.font.render("computer " + i, True, colors.white) for i in range(0,5)]

        pygame.draw.rect(self.__screen, (50, 100, 80), self.deck_space)
        pygame.draw.rect(self.__screen, (80, 120, 80), self.user_space)
        pygame.draw.rect(self.__screen, (50, 100, 80), self.deck_space)

        self.__button_text.append(self.font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[-1].bottom = self.__screen.get_rect().centery / 5

        self.__button_text.append(self.font.render("Start Game", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.user_space.centerx
        self.__button_rect[-1].centery = self.user_space.centery

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
        # 화면 검은색 채우기
        self.__screen.fill(colors.black)
        self.draw_bot_names(self.bots_space, self.bot_names_rects, self.bot_names, self.bot_name_inputs)
        self.edit_bot_name(pygame.mouse.get_pos, self.bot_names_rects, self.bot_names, self.bot_name_inputs)

        return None


    # 봇 이름 수정을 위한 입력 박스 생성 함수
    def create_input_box(self, pos, size, text):
        input_box = pygame.Rect(pos, size)
        input_text = self.font.render(text, True, colors.black)
        return input_box, input_text
    
    # 봇 이름 수정 함수
    def edit_bot_name(self, mouse_pos, bot_name_areas, bot_names, bot_name_inputs):
        for i in range(len(bot_name_areas)):
            if bot_name_areas[i].collidepoint(mouse_pos):
                # 마우스 클릭시 봇 이름 수정 가능한 입력 박스 생성
                bot_name_inputs[i] = self.create_input_box(bot_name_areas[i].topleft, bot_name_areas[0].size, bot_names[i])
            else:
                # 다른 곳을 클릭하면 입력 박스 삭제
                bot_name_inputs[i] = None

    # 봇 이름 출력 함수
    def draw_bot_names(self, bot_areas, bot_name_areas, bot_names, bot_name_inputs):
        for i in range(len(bot_areas)):
            # 봇 이름 출력
            bot_name_text = self.font.render(bot_names[i], True, colors.black)
            bot_name_pos = bot_name_areas[i].topleft
            self.__screen.blit(bot_name_text, bot_name_pos)

            # 봇 이름 수정 입력 박스 출력
            if bot_name_inputs[i]:
                pygame.draw.rect(self.__screen, colors.white, bot_name_inputs[i][0])
                self.__screen.blit(bot_name_inputs[i][1], bot_name_inputs[i][0].topleft)

    
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_text)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    return self.__button_func(i)

        return "continue"
    
    def __button_func(self, i):
        if i == 0:
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="main"))
        else:
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="gameui"))
        return None
