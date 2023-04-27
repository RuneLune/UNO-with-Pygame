from overrides import overrides
import pygame

from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from gameobj.scene2.colorcard import ColorCard
from metaclass.singleton import SingletonMeta
import util.colors as color
from util.resource_manager import font_resource


class Scene2(Scene, metaclass=SingletonMeta):
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
        card_size = (screen_rect.height * 3 // 40, screen_rect.height // 10)

        self.background = GameObject(
            background_surface, "Scene2_Background", z_index=-999
        )
        self.title_text = TextObject(
            "Scene2", title_font, color.dark_gray, "Scene2_TitleText", z_index=-900
        )
        self.back_button = TextButtonObject(
            "Back to Previous Scene",
            menu_font,
            color.white,
            "Scene2_BackButton",
            z_index=999,
        )
        self.red_card = ColorCard(
            pygame.Surface(card_size),
            "Scene2_RedCard",
            -1,
            -1,
            screen_rect.height * 1 // 40,
            screen_rect.height // 2,
            1,
        )
        self.green_card = ColorCard(
            pygame.Surface(card_size),
            "Scene2_GreenCard",
            -1,
            -1,
            screen_rect.height * 5 // 40,
            screen_rect.height // 2,
            1,
        )
        self.blue_card = ColorCard(
            pygame.Surface(card_size),
            "Scene2_BlueCard",
            -1,
            -1,
            screen_rect.height * 9 // 40,
            screen_rect.height // 2,
            1,
        )

        self.title_text.rect.center = screen_rect.center
        self.back_button.rect.topleft = (
            screen_rect.width // 20,
            screen_rect.height // 20,
        )
        self.back_button.change_highlighting_color(color.dark_red)
        self.red_card.color = color.red
        self.green_card.color = color.green
        self.blue_card.color = color.blue

        self.back_button.on_mouse_up_as_button = (
            lambda: self.scene_manager.load_previous_scene()
        )

        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.back_button)
        self.instantiate(self.red_card)
        self.instantiate(self.green_card)
        self.instantiate(self.blue_card)

        return None
