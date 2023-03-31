import pygame
import colors

from user import User
from bot import Bot
from cards import Cards
from game import Game

class Game_UI:
    def __init__(self, settings):
        self.game = Game()
        self.cards = Cards(settings)
        self.settings = settings

        # load user and bot object
        self.players = self.game.get_players()
        self.bots = []

        # discrete user and computer
        for player in self.players:
            if player.get_name() == "User": # 이름 변경에따른 코드 수정 필요
                self.user = player
            else:
                self.bots.append(player)

        self.cards.refresh()

        self.screen_size = settings.get_screen_resolution()
        self.screen = pygame.display.set_mode(self.screen_size)

        self.card_size = self.cards.get_card_image(1).get_rect().size

    def render(self):
        # each space's size,position definition
        deck_space_size = (self.screen_size[0]*(3/4),self.screen_size[1]*(2/3))
        deck_space_pos = (0,0)

        user_space_size = (self.screen_size[0]*(3/4), self.screen_size[1]*(1/3))
        self.user_space_pos = (0,self.screen_size[1]*(1/3))
        
        bots_space_size = (self.screen_size[0]*(1/4), self.screen_size[1]*(1/5))
        self.bots_space_pos = [(user_space_size[0],i * bots_space_size[1]) for i in range(0,4)]

        # space rectangular definition
        self.deck_space = pygame.rect(deck_space_pos, deck_space_size)
        self.user_space = pygame.rect(self.user_space_pos, user_space_size)
        self.bots_space = [pygame.rect(self.bots_space_pos[i], bots_space_size) for i in range(0,4)]

        # font for user, bot name
        self.font = pygame.font.Font("res/font/Travel.ttf", 20)
        self.user_name_text = self.font.render("insert_User_name", True, colors.white)
        self.bot_name_text =[self.font.render("computer " + i, True, colors.white) for i in range(0,4)]

        self.user_card_center_pos = (self.user_space.centerx - self.card_size[0]/2,
                                     self.user_space.centery - self.card_size[1]/2 )# user space 중앙에 배치
        self.bot_card_space = None

    # def refresh(self, player_count):
    #     self.game = Game(player_count)
    #     self.players = self.game.get_players()

        
    def draw(self):
        if self.pause is False:
            self.__draw_game()
            pass
        else:
            self.__darw_pause_menu()
            pass
        pass

    def __draw_game(self):
        self.screen.fill(colors.black)
        self.screen.blit()
        
        # draw spaces and text
        self.screen.blit(self.deck_space)
        self.screen.blit(self.user_space)
        self.screen.blit(self.user_name_text, self.user_space_pos)

        for i in range(0,4):
            self.screen.blit(self.bots_space[i])
            self.screen.blit(self.bot_name_text[i],self.bots_space_pos[i])
        
        # draw card space
        user_card_list = self.user.get_cards()
        user_card_num = len(user_card_list)
        bot_card_num = [len(self.bots[i].get_cards()) for i in range(len(self.bots))]

        # 플레이어가 가지고 있는 카드 이미지 로드
        user_card_image = [self.cards.get_card_image(num) for num in user_card_list]
        
        # 플레이어의 카드 그리기
        if user_card_num%2 == 0:
            for i in range(user_card_num):
                self.screen.blit(user_card_image[i],(self.user_card_center_pos[0]-(user_card_num/2)+self.card_size[0]*i,
                                                     self.user_card_center_pos[1]))
        else:
            for i in range(user_card_num):
                self.screen.blit(user_card_image[i],(self.user_card_center_pos[0]-(user_card_num//2)+self.card_size[0]*i,
                                                     self.user_card_center_pos[1]))

    def __darw_pause_menu(self):
        pass

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
        pass

    def __handle_pause_menu(self, event):
        # 일시정지 메뉴 이벤트 처리
        # 계속하기 버튼 클릭하면
        # 1. self.pause를 False로
        # 2. 모든 타이머 시작(self.game.resume_timer())
        pass
