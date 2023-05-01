from overrides import overrides
import pygame

from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
# from metaclass.singleton import SingletonMeta
import util.colors as color


class Scene1(Scene):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.black)
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 2
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 12
        )

        self.background = GameObject(
            background_surface, "Scene1_Background", z_index=-999
        )
        self.title_text = TextObject(
            "Scene1", title_font, color.dark_gray, "Scene1_TitleText", z_index=-900
        )
        self.start_button = TextButtonObject(
            "Goto Scene2", menu_font, color.white, "Scene1_StartButton", z_index=999
        )

        self.title_text.rect.center = screen_rect.center
        self.start_button.rect.topleft = (screen_rect.width // 20, screen_rect.height // 20)
        self.start_button.change_highlighting_color(color.dark_red)

        self.start_button.on_mouse_up_as_button = lambda: self.scene_manager.load_scene(
            "scene2"
        )

        # 장면에 게임 오브젝트 추가
        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.start_button)

        return None
