from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from manager.lobbymgr import LobbyManager
from gameobj.gamelobby.keyinput import KeyInput
from gameobj.gamelobby.nametext import NameText


class GameLobby(Scene):
    @overrides
    def start(self) -> None:
        # Background Surface
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.black)
        self.lobby_manager = LobbyManager()

        # Font
        small_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )
        edit_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 14
        )
        big_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 10
        )

        # Deck Surface
        deck_surface = pygame.Surface(
            (screen_rect.width * (3 / 4), screen_rect.height * (2 / 3))
        )
        deck_surface.fill((50, 100, 80))

        # User Surface
        user_surface = pygame.Surface(
            (screen_rect.width * (3 / 4), screen_rect.height * (1 / 3))
        )
        user_surface.fill((80, 120, 80))
        pygame.draw.rect(user_surface, color.white, user_surface.get_rect(), width=2)

        # Start Surface
        start_surface = pygame.Surface(
            (user_surface.get_width() * (2 / 3), user_surface.get_height() * (2 / 3))
        )
        start_surface.fill((196, 216, 214))

        # Bot Surface
        self.bot1_surface = pygame.Surface(
            (screen_rect.width * (1 / 4), screen_rect.height * (1 / 5))
        )
        self.bot1_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot1_surface, color.red, self.bot1_surface.get_rect(), width=2
        )
        self.bot1_text = TextObject(
            "CPU 1", small_font, color.white, "GameLobby_Bot1Text", z_index=1000
        )
        self.bot1_surface.blit(self.bot1_text.image, self.bot1_text.rect)

        self.bot2_surface = pygame.Surface(
            (screen_rect.width * (1 / 4), screen_rect.height * (1 / 5))
        )
        self.bot2_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot2_surface, color.red, self.bot2_surface.get_rect(), width=2
        )
        self.bot2_text = TextObject(
            "CPU 2", small_font, color.white, "GameLobby_Bot2Text", z_index=1000
        )
        self.bot2_surface.blit(self.bot2_text.image, self.bot2_text.rect)

        self.bot3_surface = pygame.Surface(
            (screen_rect.width * (1 / 4), screen_rect.height * (1 / 5))
        )
        self.bot3_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot3_surface, color.red, self.bot3_surface.get_rect(), width=2
        )
        self.bot3_text = TextObject(
            "CPU 3", small_font, color.white, "GameLobby_Bot3Text", z_index=1000
        )
        self.bot3_surface.blit(self.bot3_text.image, self.bot3_text.rect)

        self.bot4_surface = pygame.Surface(
            (screen_rect.width * (1 / 4), screen_rect.height * (1 / 5))
        )
        self.bot4_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot4_surface, color.red, self.bot4_surface.get_rect(), width=2
        )
        self.bot4_text = TextObject(
            "CPU 4", small_font, color.white, "GameLobby_Bot4Text", z_index=1000
        )
        self.bot4_surface.blit(self.bot4_text.image, self.bot4_text.rect)

        self.bot5_surface = pygame.Surface(
            (screen_rect.width * (1 / 4), screen_rect.height * (1 / 5))
        )
        self.bot5_surface.fill((50, 50, 50))
        pygame.draw.rect(
            self.bot5_surface, color.red, self.bot5_surface.get_rect(), width=2
        )
        self.bot5_text = TextObject(
            "CPU 5", small_font, color.white, "GameLobby_Bot5Text", z_index=1000
        )
        self.bot5_surface.blit(self.bot5_text.image, self.bot5_text.rect)

        # Empty Surface
        self.empty_surface = pygame.Surface(
            (screen_rect.width * (1 / 4), screen_rect.height * (1 / 5))
        )
        self.empty_surface.fill(color.white)
        pygame.draw.rect(
            self.empty_surface,
            color.black,
            self.empty_surface.get_rect(),
            int(screen_rect.height * (1 / 100)),
        )
        self.empty_text = TextObject(
            "Empty", small_font, color.light_gray, "GameLobby_EmptyText", z_index=1000
        )
        self.empty_text.rect.center = self.empty_surface.get_rect().center
        self.empty_surface.blit(self.empty_text.image, self.empty_text.rect)

        self.bot1_real_surface = (
            self.empty_surface
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot1"]
            else self.bot1_surface
        )
        self.bot2_real_surface = (
            self.empty_surface
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot2"]
            else self.bot2_surface
        )
        self.bot3_real_surface = (
            self.empty_surface
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot3"]
            else self.bot3_surface
        )
        self.bot4_real_surface = (
            self.empty_surface
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot4"]
            else self.bot4_surface
        )
        self.bot5_real_surface = (
            self.empty_surface
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot5"]
            else self.bot5_surface
        )

        self.invisible_surface = pygame.Surface((screen_rect.width, screen_rect.height))
        self.invisible_surface.set_alpha(0)

        # Is the user editing their name?
        self.user_name_editing = False

        # Create the objects
        self.background = GameObject(
            background_surface, "GameLobby_Background", z_index=-999
        )
        self.deck_space = GameObject(deck_surface, "GameLobby_Deck", z_index=999)
        self.back_button = TextButtonObject(
            "◀ Back", small_font, color.white, "GameLobby_BackButton", z_index=1000
        )
        self.edit_text = TextObject(
            "Press Enter to edit the name",
            edit_font,
            color.white,
            "GameLobby_EditText",
            z_index=1000,
        )
        self.name_text = NameText()
        # self.name_text = TextObject(
        #     self.lobby_manager.get_game_settings()["user_name"],
        #     middle_font,
        #     color.white,
        #     "GameLobby_NameText",
        #     z_index=1000,
        # )
        self.user_space = GameObject(user_surface, "GameLobby_User", z_index=999)
        self.start_button = GameObject(
            start_surface, "GameLobby_StartButton", z_index=1000
        )
        self.start_text = TextButtonObject(
            "Start Game", big_font, color.white, "GameLobby_StartText", z_index=1001
        )
        self.bot1_button = GameObject(
            self.bot1_real_surface, "GameLobby_Bot1Button", z_index=1000
        )
        self.bot2_button = GameObject(
            self.bot2_real_surface, "GameLobby_Bot2Button", z_index=1000
        )
        self.bot3_button = GameObject(
            self.bot3_real_surface, "GameLobby_Bot3Button", z_index=1000
        )
        self.bot4_button = GameObject(
            self.bot4_real_surface, "GameLobby_Bot4Button", z_index=1000
        )
        self.bot5_button = GameObject(
            self.bot5_real_surface, "GameLobby_Bot5Button", z_index=1000
        )

        self.invisible_background = GameObject(
            self.invisible_surface, "GameLobby_UnvisibleBackground", z_index=-2000
        )
        self.invisible_background.disable()

        # Position of the objects
        self.deck_space.rect.topleft = (0, 0)
        self.back_button.rect.bottomright = (
            screen_rect.centerx / 3,
            screen_rect.centery / 5,
        )
        self.edit_text.rect.center = (
            self.deck_space.rect.centerx,
            self.deck_space.rect.bottom * (1 / 3),
        )
        self.name_text.rect.center = (
            self.deck_space.rect.centerx,
            self.deck_space.rect.bottom * (2 / 3),
        )
        self.user_space.rect.topleft = (0, deck_surface.get_height())
        self.start_button.rect.center = (
            self.user_space.rect.centerx,
            self.user_space.rect.centery,
        )
        self.start_text.rect.center = self.start_button.rect.center
        self.bot1_button.rect.topleft = (self.user_space.rect.right, 0)
        self.bot2_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (1 / 5),
        )
        self.bot3_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (2 / 5),
        )
        self.bot4_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (3 / 5),
        )
        self.bot5_button.rect.topleft = (
            self.user_space.rect.right,
            screen_rect.height * (4 / 5),
        )

        self.invisible_background.rect.topleft = (0, 0)

        def key_down(key):
            if key == pygame.K_RETURN:
                self.editName()
            elif key == pygame.K_ESCAPE:
                self.scene_manager.load_previous_scene()
            else:
                return False

        # self.background.on_key_down = lambda key: key_down(key)
        self.back_button.on_click = lambda: self.scene_manager.load_previous_scene()
        self.name_text.on_mouse_up_as_button = lambda: self.editName()
        self.start_button.on_mouse_up_as_button = lambda: self.scene_manager.load_scene(
            "game_scene"
        )
        self.start_text.on_click = lambda: self.scene_manager.load_scene("game_scene")
        # self.bot1_button.on_mouse_up_as_button = lambda: self.bot1Clicked()
        self.bot2_button.on_mouse_up_as_button = lambda: self.bot2Clicked()
        self.bot3_button.on_mouse_up_as_button = lambda: self.bot3Clicked()
        self.bot4_button.on_mouse_up_as_button = lambda: self.bot4Clicked()
        self.bot5_button.on_mouse_up_as_button = lambda: self.bot5Clicked()

        # self.invisible_background.on_mouse_up_as_button = lambda: self.editName()
        # self.invisible_background.on_key_down = lambda: self.editName()

        self.instantiate(self.background)
        self.instantiate(self.deck_space)
        self.instantiate(self.back_button)
        self.instantiate(self.edit_text)
        self.instantiate(self.name_text)
        self.instantiate(self.user_space)
        self.instantiate(self.start_button)
        self.instantiate(self.start_text)
        self.instantiate(self.bot1_button)
        self.instantiate(self.bot2_button)
        self.instantiate(self.bot3_button)
        self.instantiate(self.bot4_button)
        self.instantiate(self.bot5_button)
        self.instantiate(self.invisible_background)
        self.key_input = KeyInput().attach_mgr(self.scene_manager)
        self.key_input.reset()
        self.instantiate(self.key_input)

        return None

    def editName(self):
        rect = pygame.Rect(self.name_text.rect)
        rect.topleft = (0, 0)
        if not self.key_input.changing_name:
            pygame.draw.rect(self.name_text.image, color.white, rect, 2)
            self.key_input.changing_name = True
            # self.user_name_editing = True
        else:
            pygame.draw.rect(self.name_text.image, (50, 100, 80), rect, 2)
            self.key_input.changing_name = False
            # self.user_name_editing = False
        return None

    # def bot1Clicked(self):
    #     self.lobby_manager.bot1_toggle()
    #     if self.lobby_manager.get_game_settings()["active_bots"]["bot1"]:
    #         self.bot1_button.image = self.bot1_surface
    #     else:
    #         self.bot1_button.image = self.empty_surface
    #     return None

    def bot2Clicked(self):
        if (
            self.lobby_manager.get_game_settings()["active_bots"]["bot1"]
            and not self.lobby_manager.get_game_settings()["active_bots"]["bot3"]
        ):
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot2"]:
                self.bot2_button.image = self.bot2_surface
                self.lobby_manager.set_player_count(3)
            else:
                self.bot2_button.image = self.empty_surface
                self.lobby_manager.set_player_count(2)
            self.lobby_manager.bot2_toggle()
        else:
            pass
        return None

    def bot3Clicked(self):
        if (
            self.lobby_manager.get_game_settings()["active_bots"]["bot2"]
            and not self.lobby_manager.get_game_settings()["active_bots"]["bot4"]
        ):
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot3"]:
                self.bot3_button.image = self.bot3_surface
                self.lobby_manager.set_player_count(4)
            else:
                self.bot3_button.image = self.empty_surface
                self.lobby_manager.set_player_count(3)
            self.lobby_manager.bot3_toggle()
        else:
            pass
        return None

    def bot4Clicked(self):
        if (
            self.lobby_manager.get_game_settings()["active_bots"]["bot3"]
            and not self.lobby_manager.get_game_settings()["active_bots"]["bot5"]
        ):
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot4"]:
                self.bot4_button.image = self.bot4_surface
                self.lobby_manager.set_player_count(5)
            else:
                self.bot4_button.image = self.empty_surface
                self.lobby_manager.set_player_count(4)
            self.lobby_manager.bot4_toggle()
        else:
            pass
        return None

    def bot5Clicked(self):
        if self.lobby_manager.get_game_settings()["active_bots"]["bot4"]:
            if not self.lobby_manager.get_game_settings()["active_bots"]["bot5"]:
                self.bot5_button.image = self.bot5_surface
                self.lobby_manager.set_player_count(6)
            else:
                self.bot5_button.image = self.empty_surface
                self.lobby_manager.set_player_count(5)
            self.lobby_manager.bot5_toggle()
        else:
            pass
        return None
