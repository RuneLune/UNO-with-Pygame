import pygame
import colors

from user import User
from bot import Bot
from cards import Cards
from game import Game

class Game_UI:
    def __init__(self, settings):
        # self.user = User()
        # self.bot = Bot()
        self.game = Game(settings)
        self.cards = Cards(settings)
        self.settings = settings

        # load user and bot object
        self.players = self.game.get_players()
        self.bots = []

        # discrete user and computer
        for player in self.players:
            if player.get_name() == "User":
                self.user = player
            else:
                self.bots.append(player)

        self.cards.refresh()

        self.screen_size = settings.get_screen_resolution()
        self.screen = pygame.display.set_mode(self.screen_size)

        self.user_card_list = self.game.get_cards()
        self.bot_card_list = self.bot.get_cards()

    def render(self):
        # each space's size,position definition
        deck_space_size = (self.screen_size[0]*(3/4),self.screen_size[1]*(2/3))
        deck_space_pos = (0,0)

        user_space_size = (self.screen_size[0]*(3/4), self.screen_size[1]*(1/3))
        self.user_space_pos = (0,self.screen_size[1]*(1/3))
        
        bots_space_size = (self.screen_size[0]*(1/4), self.screen_size[1]*(9/4))
        self.bots_space_pos = [(user_space_size[0],i * bots_space_size[1]) for i in range(0,4)]

        # space rectangular definition
        self.deck_space = pygame.rect(deck_space_pos, deck_space_size)
        self.user_space = pygame.rect(self.user_space_pos, user_space_size)
        self.bots_space = [pygame.rect(self.bots_space_pos[i], bots_space_size) for i in range(0,4)]

        # font for user, bot name
        self.font = pygame.font.Font("res/font/Travel.ttf", 20)
        self.user_name_text = self.font.render("insert_User_name", True, colors.white)
        self.bot_name_text =[self.font.render("computer " + i, True, colors.white) for i in range(0,4)]

        self.user_card_space = None# user space 중앙에 배치
        self.bot_card_space

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
        bot_card_list = self.bot.get_cards()

        user_card_image = [self.cards.get_card_image(num) for num in user_card_list]

        for i in range(len(user_card_list)):
            self.screen.blit(user_card_image[i],)
        
        pass

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
