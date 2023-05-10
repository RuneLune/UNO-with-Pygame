from overrides import overrides
import pygame

from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
import util.colors as color


class TestScene(Scene):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.black)
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 5
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 12
        )

        self.background = GameObject(
            background_surface, "TestScene_Background", z_index=-999
        )
        self.title_text = TextObject(
            "Test Scene", title_font, color.gray, "TestScene_TitleText", z_index=-900
        )
        self.back_button = TextButtonObject(
            "Back to Previous Scene",
            menu_font,
            color.white,
            "TestScene_BackButton",
            z_index=999,
        )

        self.title_text.rect.center = screen_rect.center
        self.back_button.rect.topleft = (
            screen_rect.width // 20,
            screen_rect.height // 20,
        )
        self.back_button.change_highlighting_color(color.light_gray)

        self.back_button.on_mouse_up_as_button = (
            lambda: self.scene_manager.load_previous_scene()
        )

        # 장면에 게임 오브젝트 추가
        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.back_button)

        return None
