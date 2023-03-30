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
        self.settings = settings

        self.screen_size = settings.get_screen_resolution()
        self.screen = pygame.display.set_mode(self.screen_size)
        return super().__init__()

    def render(self):
        