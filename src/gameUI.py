import pygame
import colors

from user import User
from bot import Bot
from cards import Cards

class Game_UI:
    def __init__(self,settings):
        self.user = User()
        self.bot = Bot()
        self.cards = Cards()
        self.settings = settings

        self.cards.refresh()

        self.screen_size = settings.get_screen_resolution()
        self.screen = pygame.display.set_mode(self.screen_size)

        self.user_card_list = self.user.get_cards()
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

        self.user_card_space = # user space 중앙에 배치
        self.bot_card_space

        
    def draw(self):
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

    def handle(self, event):
        None
        