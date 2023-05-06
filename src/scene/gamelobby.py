from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from manager.lobbymgr import LobbyManager
from metaclass.singleton import SingletonMeta

class Gamelobby(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        # Background Surface
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.BLACK)

        # Font
        small_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        middle_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 15
        )
        edit_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 14
        )
        big_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 10
        )

        # Deck Surface
        deck_surface = pygame.Surface((screen_rect.width * (3 / 4), screen_rect.height * (2 / 3)))
        deck_surface.fill((50, 100, 80))

        # User Surface
        user_surface = pygame.Surface((screen_rect.width * (3 / 4), screen_rect.height * (1 / 3)))
        user_surface.fill((80, 120, 80))
        pygame.draw.rect(
            user_surface,
            color.white,
            user_surface.get_rect(),
            width=2
        )

        # Start Surface
        start_surface = pygame.Surface((user_surface.get_width() * (2 / 3), user_surface.get_height * (2 / 3)))
        start_surface.fill((196, 216, 214))
        self.start_text = TextObject(
            "Start Game", big_font, color.white, "GameLobby_StartText", z_index=1001
        )
        start_surface.blit(self.start_text.image, self.start_text.rect)

        # Bot Surface
        self.bot1_surface = pygame.Surface((screen_rect.width * (1 / 4), screen_rect.height * (1 / 5)))
        self.bot1_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot1_surface,
            color.red,
            self.bot1_surface.get_rect(),
            width=2
        )
        self.bot1_text = TextObject(
            "CPU 1", small_font, color.white, "GameLobby_Bot1Text", z_index=1000
        )
        self.bot1_surface.blit(self.bot1_text.image, self.bot1_text.rect)

        self.bot2_surface = pygame.Surface((screen_rect.width * (1 / 4), screen_rect.height * (1 / 5)))
        self.bot2_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot2_surface,
            color.red,
            self.bot2_surface.get_rect(),
            width=2
        )
        self.bot2_text = TextObject(
            "CPU 2", small_font, color.white, "GameLobby_Bot2Text", z_index=1000
        )
        self.bot2_surface.blit(self.bot2_text.image, self.bot2_text.rect)

        self.bot3_surface = pygame.Surface((screen_rect.width * (1 / 4), screen_rect.height * (1 / 5)))
        self.bot3_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot3_surface,
            color.red,
            self.bot3_surface.get_rect(),
            width=2
        )
        self.bot3_text = TextObject(
            "CPU 3", small_font, color.white, "GameLobby_Bot3Text", z_index=1000
        )
        self.bot3_surface.blit(self.bot3_text.image, self.bot3_text.rect)

        self.bot4_surface = pygame.Surface((screen_rect.width * (1 / 4), screen_rect.height * (1 / 5)))
        self.bot4_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot4_surface,
            color.red,
            self.bot4_surface.get_rect(),
            width=2
        )
        self.bot4_text = TextObject(
            "CPU 4", small_font, color.white, "GameLobby_Bot4Text", z_index=1000
        )
        self.bot4_surface.blit(self.bot4_text.image, self.bot4_text.rect)

        self.bot5_surface = pygame.Surface((screen_rect.width * (1 / 4), screen_rect.height * (1 / 5)))
        self.bot5_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot5_surface,
            color.red,
            self.bot5_surface.get_rect(),
            width=2
        )
        self.bot5_text = TextObject(
            "CPU 5", small_font, color.white, "GameLobby_Bot5Text", z_index=1000
        )
        self.bot5_surface.blit(self.bot5_text.image, self.bot5_text.rect)

        # Empty Surface
        self.empty_text = TextObject(
            "empty", small_font, color.light_gray, "GameLobby_EmptyText", z_index=1000
        )
        self.empty1_surface = pygame.Surface(self.bot1_surface.get_size())
        self.empty1_surface.fill(color.white)
        pygame.draw.rect(
            self.empty1_surface,
            color.black,
            self.empty1_surface.get_rect(),
            int(screen_rect.height * (1 / 100))
        )
        self.empty1_surface.blit(self.empty_text.image, self.empty_text.rect)

        self.empty2_surface = pygame.Surface(self.bot2_surface.get_size())
        self.empty2_surface.fill(color.white)
        pygame.draw.rect(
            self.empty2_surface,
            color.black,
            self.empty2_surface.get_rect(),
            int(screen_rect.height * (1 / 100))
        )
        self.empty2_surface.blit(self.empty_text.image, self.empty_text.rect)

        self.empty3_surface = pygame.Surface(self.bot3_surface.get_size())
        self.empty3_surface.fill(color.white)
        pygame.draw.rect(
            self.empty3_surface,
            color.black,
            self.empty3_surface.get_rect(),
            int(screen_rect.height * (1 / 100))
        )
        self.empty3_surface.blit(self.empty_text.image, self.empty_text.rect)

        self.empty4_surface = pygame.Surface(self.bot4_surface.get_size())
        self.empty4_surface.fill(color.white)
        pygame.draw.rect(
            self.empty4_surface,
            color.black,
            self.empty4_surface.get_rect(),
            int(screen_rect.height * (1 / 100))
        )
        self.empty4_surface.blit(self.empty_text.image, self.empty_text.rect)

        self.empty5_surface = pygame.Surface(self.bot5_surface.get_size())
        self.empty5_surface.fill(color.white)
        pygame.draw.rect(
            self.empty5_surface,
            color.black,
            self.empty5_surface.get_rect(),
            int(screen_rect.height * (1 / 100))
        )
        self.empty5_surface.blit(self.empty_text.image, self.empty_text.rect)

        # Create the objects
        self.background = GameObject(
            background_surface, "GameLobby_Background", z_index=-999
        )
        self.deck_space = GameObject(
            deck_surface, "GameLobby_Deck", z_index=999
        )
        self.back_button = TextButtonObject(
            "Back", small_font, color.white, "GameLobby_BackButton", z_index=1000
        )
        self.edit_text = TextObject(
            "Press Enter to edit the name", edit_font, color.white, "GameLobby_EditText", z_index=1000
        )
        self.name_text = TextObject(
            # lobby_function 구현에 따른 수정 필요
        )
        self.user_space = GameObject(
            user_surface, "GameLobby_User", z_index=999
        )
        self.start_button = GameObject(
            start_surface, "GameLobby_StartButton", z_index=1000
        )
        self.bot1_button = GameObject(
            self.bot1_surface, "GameLobby_Bot1Button", z_index=1000
        )
        self.bot2_button = GameObject(
            self.empty2_surface, "GameLobby_Bot2Button", z_index=1000
        )
        self.bot3_button = GameObject(
            self.empty3_surface, "GameLobby_Bot3Button", z_index=1000
        )
        self.bot4_button = GameObject(
            self.empty4_surface, "GameLobby_Bot4Button", z_index=1000
        )
        self.bot5_button = GameObject(
            self.empty5_surface, "GameLobby_Bot5Button", z_index=1000
        )

        # Position of the objects
        self.deck_space.rect.topleft = (0, 0)
        self.back_button.rect.bottomright = (
            screen_rect.centerx / 3,
            screen_rect.centery / 5
        )
        self.edit_text.rect.center = (
            self.deck_space.rect.centerx,
            self.deck_space.rect.bottom * (1 / 3)
        )
        self.name_text.rect.center = (
            self.deck_space.rect.centerx,
            self.deck_space.rect.bottom * (2 / 3)
        )
        self.user_space.rect.topleft = (
            0,
            deck_surface.get_height()
        )
        self.start_button.rect.center = (
            self.user_space.rect.centerx,
            self.user_space.rect.centery
        )
        self.bot1_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (1 / 5)
        )
        self.bot2_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (2 / 5)
        )
        self.bot3_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (3 / 5)
        )
        self.bot4_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (4 / 5)
        )
        self.bot5_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height
        )

        self.back_button.on_click = lambda: self.scene_manager.load_previous_scene()
        self.start_button.on_click = lambda: self.scene_manager.load_scene("GameScene")
        self.start_button.on_mouse_up = lambda: self.start()
        self.bot1_button.on_click = lambda: self.bot1Clicked()
        self.bot2_button.on_click = lambda: self.bot2Clicked()
        self.bot3_button.on_click = lambda: self.bot3Clicked()
        self.bot4_button.on_click = lambda: self.bot4Clicked()
        self.bot5_button.on_click = lambda: self.bot5Clicked()

        self.instantiate(self.background)
        self.instantiate(self.deck_space)
        self.instantiate(self.back_button)
        self.instantiate(self.edit_text)
        self.instantiate(self.name_text)
        self.instantiate(self.user_space)
        self.instantiate(self.start_button)
        self.instantiate(self.bot1_button)
        self.instantiate(self.bot2_button)
        self.instantiate(self.bot3_button)
        self.instantiate(self.bot4_button)
        self.instantiate(self.bot5_button)

        return None
    
    def bot1Clicked(self):
        if LobbyManager.get_game_settings.["pressed_bots"]["bot1"]:
            self.bot1_button.image = self.bot1_surface
            LobbyManager.bot1_toggle
        else:
            self.bot1_button.image = self.empty1_surface
            LobbyManager.bot1_toggle
        return None
    
    def bot2Clicked(self):
        if LobbyManager.get_game_settings.["pressed_bots"]["bot2"]:
            self.bot2_button.image = self.bot2_surface
            LobbyManager.bot2_toggle
        else:
            self.bot2_button.image = self.empty2_surface
            LobbyManager.bot2_toggle
    
    def bot3Clicked(self):
        if LobbyManager.get_game_settings.["pressed_bots"]["bot3"]:
            self.bot3_button.image = self.bot3_surface
            LobbyManager.bot3_toggle
        else:
            self.bot3_button.image = self.empty3_surface
            LobbyManager.bot3_toggle
    
    def bot4Clicked(self):
        if LobbyManager.get_game_settings.["pressed_bots"]["bot4"]:
            self.bot4_button.image = self.bot4_surface
            LobbyManager.bot4_toggle
        else:
            self.bot4_button.image = self.empty4_surface
            LobbyManager.bot4_toggle

    def bot5Clicked(self):
        if LobbyManager.get_game_settings.["pressed_bots"]["bot5"]:
            self.bot5_button.image = self.bot5_surface
            LobbyManager.bot5_toggle
        else:
            self.bot5_button.image = self.empty5_surface
            LobbyManager.bot5_toggle