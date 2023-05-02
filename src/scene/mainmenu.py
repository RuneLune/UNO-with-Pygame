from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject


class MainMenu(Scene):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.white)
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 3
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 12
        )

        self.background = GameObject(
            background_surface, "MainMenu_Background", z_index=-999
        )
        self.title_text = TextObject(
            "UNO", title_font, color.black, "MainMenu_TitleText"
        )
        self.play_button = TextButtonObject(
            "Play", menu_font, color.black, "MainMenu_PlayButton"
        )
        self.stage_button = TextButtonObject(
            "Stage", menu_font, color.black, "MainMenu_StageButton"
        )
        self.settings_button = TextButtonObject(
            "Settings", menu_font, color.black, "MainMenu_SettingsButton"
        )
        self.quit_button = TextButtonObject(
            "Quit", menu_font, color.black, "QuitButton"
        )

        self.title_text.rect.center = (
            screen_rect.centerx,
            screen_rect.height * 3 // 10,
        )
        self.play_button.rect.center = (
            screen_rect.centerx,
            screen_rect.height * 6 // 10,
        )
        self.stage_button.rect.center = (
            screen_rect.centerx,
            screen_rect.height * 7 // 10,
        )
        self.settings_button.rect.center = (
            screen_rect.centerx,
            screen_rect.height * 8 // 10,
        )
        self.quit_button.rect.center = (
            screen_rect.centerx,
            screen_rect.height * 9 // 10,
        )

        self.play_button.on_mouse_up_as_button = lambda: self.scene_manager.load_scene(
            "game_scene"
        )
        self.stage_button.on_mouse_up_as_button = lambda: self.scene_manager.load_scene(
            "scene2"
        )
        self.settings_button.on_mouse_up_as_button = (
            lambda: self.scene_manager.load_scene("config_menu")
        )
        self.quit_button.on_mouse_up_as_button = lambda: pygame.event.post(
            pygame.event.Event(pygame.QUIT)
        )

        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.play_button)
        self.instantiate(self.stage_button)
        self.instantiate(self.settings_button)
        self.instantiate(self.quit_button)

        return None
