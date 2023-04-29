from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from config.settings_function import Settings
from gameobj.txtbtnobj import TextButtonObject
# from metaclass.singleton import SingletonMeta


class ConfigMenu(Scene):
    @overrides
    def start(self) -> None:
        self.game_objects = []
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.black)
        config = Settings().get_settings()
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 10
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 20
        )

        self.background = GameObject(
            background_surface, "ConfigMenu_Background", z_index=-999
        )
        self.title_text = TextObject(
            "Settings", title_font, color.white, "ConfigMenu_TitleText"
        )
        self.screen_size_key = TextObject(
            "Screen Size |", menu_font, color.white, "ConfigMenu_ScreenSizeKey"
        )
        self.screen_size_value = TextObject(
            config["screen_size"], menu_font, color.white, "ConfigMenu_ScreenSizeValue"
        )
        self.screen_size_left_button = TextButtonObject(
            "<",
            menu_font,
            color.white,
            "ConfigMenu_ScreenSizeLeftBtn",
        )
        self.screen_size_right_button = TextButtonObject(
            ">",
            menu_font,
            color.white,
            "ConfigMenu_ScreenSizeRightBtn",
        )
        self.fullscreen_key = TextObject(
            "Fullscreen |", menu_font, color.white, "ConfigMenu_FullscreenKey"
        )
        self.fullscreen_value = TextObject(
            "On" if config.get("fullscreen") is True else "Off",
            menu_font,
            color.white,
            "ConfigMenu_FullscreenValue",
        )
        self.fullscreen_left_button = TextButtonObject(
            "<",
            menu_font,
            color.white,
            "ConfigMenu_FullscreenLeftBtn",
        )
        self.fullscreen_right_button = TextButtonObject(
            ">",
            menu_font,
            color.white,
            "ConfigMenu_FullscreenRightBtn",
        )
        self.key_settings_key = TextObject(
            "Key Settings |", menu_font, color.white, "ConfigMenu_KeySettingsKey"
        )
        self.left_key = TextObject(
            "Left |", menu_font, color.white, "ConfigMenu_LeftKey"
        )
        self.left_value = TextObject(
            pygame.key.name(config["key_settings"]["left"]),
            menu_font,
            color.white,
            "ConfigMenu_LeftValue",
        )
        self.right_key = TextObject(
            "Right |", menu_font, color.white, "ConfigMenu_RightKey"
        )
        self.right_value = TextObject(
            pygame.key.name(config["key_settings"]["right"]),
            menu_font,
            color.white,
            "ConfigMenu_RightValue",
        )
        self.up_key = TextObject("Up |", menu_font, color.white, "ConfigMenu_UpKey")
        self.up_value = TextObject(
            pygame.key.name(config["key_settings"]["up"]),
            menu_font,
            color.white,
            "ConfigMenu_UpValue",
        )
        self.down_key = TextObject(
            "Down |", menu_font, color.white, "ConfigMenu_DownKey"
        )
        self.down_value = TextObject(
            pygame.key.name(config["key_settings"]["down"]),
            menu_font,
            color.white,
            "ConfigMenu_DownValue",
        )
        self.select_key = TextObject(
            "Select |", menu_font, color.white, "ConfigMenu_SelectKey"
        )
        self.select_value = TextObject(
            pygame.key.name(config["key_settings"]["select"]),
            menu_font,
            color.white,
            "ConfigMenu_SelectValue",
        )
        self.cancel_key = TextObject(
            "Cancel |", menu_font, color.white, "ConfigMenu_CancelKey"
        )
        self.cancel_value = TextObject(
            pygame.key.name(config["key_settings"]["cancel"]),
            menu_font,
            color.white,
            "ConfigMenu_CancelValue",
        )
        self.colorblind_mode_key = TextObject(
            "Colorblind Mode |", menu_font, color.white, "ConfigMenu_ColorblindModeKey"
        )
        self.colorblind_mode_value = TextObject(
            "On" if config["colorblind_mode"] else "Off",
            menu_font,
            color.white,
            "ConfigMenu_ColorblindModeValue",
        )
        self.colorblind_left_button = TextButtonObject(
            "<",
            menu_font,
            color.white,
            "ConfigMenu_ColorblindLeftBtn",
        )
        self.colorblind_right_button = TextButtonObject(
            ">",
            menu_font,
            color.white,
            "ConfigMenu_ColorblindRightBtn",
        )

        self.title_text.rect.centerx = screen_rect.centerx
        self.title_text.rect.bottom = screen_rect.height // 8
        self.screen_size_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 3 // 16,
        )
        self.screen_size_value.rect.centerx = screen_rect.width * 5 // 8
        self.screen_size_value.rect.top = screen_rect.height * 3 // 16
        self.screen_size_left_button.rect.left = screen_rect.width * 4 // 8
        self.screen_size_left_button.rect.top = screen_rect.height * 3 // 16
        self.screen_size_right_button.rect.right = screen_rect.width * 6 // 8
        self.screen_size_right_button.rect.top = screen_rect.height * 3 // 16
        self.fullscreen_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 4 // 16,
        )
        self.fullscreen_value.rect.centerx = screen_rect.width * 5 // 8
        self.fullscreen_value.rect.top = screen_rect.height * 4 // 16
        self.fullscreen_left_button.rect.left = screen_rect.width * 4 // 8
        self.fullscreen_left_button.rect.top = screen_rect.height * 4 // 16
        self.fullscreen_right_button.rect.right = screen_rect.width * 6 // 8
        self.fullscreen_right_button.rect.top = screen_rect.height * 4 // 16
        self.key_settings_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 5 // 16,
        )
        self.left_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 6 // 16,
        )
        self.left_value.rect.centerx = screen_rect.width * 5 // 8
        self.left_value.rect.top = screen_rect.height * 6 // 16
        self.right_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 7 // 16,
        )
        self.right_value.rect.centerx = screen_rect.width * 5 // 8
        self.right_value.rect.top = screen_rect.height * 7 // 16
        self.up_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 8 // 16,
        )
        self.up_value.rect.centerx = screen_rect.width * 5 // 8
        self.up_value.rect.top = screen_rect.height * 8 // 16
        self.down_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 9 // 16,
        )
        self.down_value.rect.centerx = screen_rect.width * 5 // 8
        self.down_value.rect.top = screen_rect.height * 9 // 16
        self.select_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 10 // 16,
        )
        self.select_value.rect.centerx = screen_rect.width * 5 // 8
        self.select_value.rect.top = screen_rect.height * 10 // 16
        self.cancel_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 11 // 16,
        )
        self.cancel_value.rect.centerx = screen_rect.width * 5 // 8
        self.cancel_value.rect.top = screen_rect.height * 11 // 16
        self.colorblind_mode_key.rect.topright = (
            screen_rect.centerx * 9 // 10,
            screen_rect.height * 12 // 16,
        )
        self.colorblind_mode_value.rect.centerx = screen_rect.width * 5 // 8
        self.colorblind_mode_value.rect.top = screen_rect.height * 12 // 16
        self.colorblind_left_button.rect.left = screen_rect.width * 4 // 8
        self.colorblind_left_button.rect.top = screen_rect.height * 12 // 16
        self.colorblind_right_button.rect.right = screen_rect.width * 6 // 8
        self.colorblind_right_button.rect.top = screen_rect.height * 12 // 16

        self.screen_size_left_button.on_mouse_up = lambda: self.start()
        self.screen_size_right_button.on_mouse_up = lambda: self.start()
        self.screen_size_left_button.on_click = (
            lambda: Settings().decrease_screen_size()
        )
        self.screen_size_right_button.on_click = (
            lambda: Settings().increase_screen_size()
        )
        self.fullscreen_left_button.on_mouse_up = lambda: self.start()
        self.fullscreen_right_button.on_mouse_up = lambda: self.start()
        self.fullscreen_left_button.on_click = (
            lambda: Settings().toggle_fullscreen()
        )
        self.fullscreen_right_button.on_click = (
            lambda: Settings().toggle_fullscreen()
        )
        self.colorblind_left_button.on_mouse_up = lambda: self.start()
        self.colorblind_right_button.on_mouse_up = lambda: self.start()
        self.colorblind_left_button.on_click = (
            lambda: Settings().toggle_colorblind_mode()
        )
        self.colorblind_right_button.on_click = (
            lambda: Settings().toggle_colorblind_mode()
        )

        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.screen_size_key)
        self.instantiate(self.screen_size_value)
        self.instantiate(self.screen_size_left_button)
        self.instantiate(self.screen_size_right_button)
        self.instantiate(self.fullscreen_key)
        self.instantiate(self.fullscreen_value)
        self.instantiate(self.fullscreen_left_button)
        self.instantiate(self.fullscreen_right_button)
        self.instantiate(self.key_settings_key)
        self.instantiate(self.left_key)
        self.instantiate(self.left_value)
        self.instantiate(self.right_key)
        self.instantiate(self.right_value)
        self.instantiate(self.up_key)
        self.instantiate(self.up_value)
        self.instantiate(self.down_key)
        self.instantiate(self.down_value)
        self.instantiate(self.select_key)
        self.instantiate(self.select_value)
        self.instantiate(self.cancel_key)
        self.instantiate(self.cancel_value)
        self.instantiate(self.colorblind_mode_key)
        self.instantiate(self.colorblind_mode_value)
        self.instantiate(self.colorblind_left_button)
        self.instantiate(self.colorblind_right_button)

        return None
