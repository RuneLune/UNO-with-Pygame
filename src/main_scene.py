import pygame
from overrides import overrides
from typing import Final, List, Tuple

import colors
import events
from settings_function import Settings
from sound import SoundManager
from scene import Scene
from resource_manager import font_resource


class Main_Scene(Scene):
    MAX_Inst: Final[int] = 1
    Inst_created: int = 0

    @overrides
    def __new__(cls, *args, **kwargs):
        if cls.Inst_created >= cls.MAX_Inst:
            raise ValueError("Cannot create more Main Scene")
        cls.Inst_created += 1
        return super(Main_Scene, cls).__new__(cls)

    @overrides
    def __init__(self, settings: Settings, sound_manager: SoundManager) -> None:
        self.__menu_options: List[str] = ["Start", "Story", "Settings", "Quit"]
        self.__settings: Settings = settings
        self.sounds: SoundManager = sound_manager
        self.refresh()
        return None

    @overrides
    def render(self) -> None:
        screen_size: Tuple[int, int] = self.__settings.get_screen_resolution()

        self.__title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 3)
        )
        self.__menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"),
            round(screen_size[1] / (3.3 * len(self.__menu_options))),
        )
        self.__key_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 20)
        )

        self.__title_text = self.__title_font.render("UNO", True, colors.black)
        self.__title_rect = self.__title_text.get_rect()
        self.__title_rect.centerx = self.__screen.get_rect().centerx
        self.__title_rect.bottom = self.__screen.get_rect().centery

        for i in range(len(self.__menu_options)):
            self.__menu_text.append(
                self.__menu_font.render(self.__menu_options[i], True, colors.black)
            )
            self.__menu_rect.append(self.__menu_text[i].get_rect())
            self.__menu_rect[i].centerx = self.__screen.get_rect().centerx
            self.__menu_rect[
                i
            ].top = self.__screen.get_rect().centery + i * screen_size[1] / (
                3 * len(self.__menu_options)
            )
        self.__selected_rect = pygame.Rect(
            0, 0, screen_size[0] / 3, screen_size[1] / (3 * len(self.__menu_options))
        )

        key_left = pygame.key.name(
            self.__settings.get_settings().get("key_settings", None).get("left", None)
        )
        key_right = pygame.key.name(
            self.__settings.get_settings().get("key_settings", None).get("right", None)
        )
        key_up = pygame.key.name(
            self.__settings.get_settings().get("key_settings", None).get("up", None)
        )
        key_down = pygame.key.name(
            self.__settings.get_settings().get("key_settings", None).get("down", None)
        )
        key_select = pygame.key.name(
            self.__settings.get_settings().get("key_settings", None).get("select", None)
        )
        key_cancel = pygame.key.name(
            self.__settings.get_settings().get("key_settings", None).get("cancel", None)
        )

        self.__key_settings_text.append(
            self.__key_font.render(f"Left: {key_left}", True, colors.black)
        )
        self.__key_settings_text.append(
            self.__key_font.render(f"Right: {key_right}", True, colors.black)
        )
        self.__key_settings_text.append(
            self.__key_font.render(f"Up: {key_up}", True, colors.black)
        )
        self.__key_settings_text.append(
            self.__key_font.render(f"Down: {key_down}", True, colors.black)
        )
        self.__key_settings_text.append(
            self.__key_font.render(f"Select: {key_select}", True, colors.black)
        )
        self.__key_settings_text.append(
            self.__key_font.render(f"Cancel: {key_cancel}", True, colors.black)
        )

        for i in range(len(self.__key_settings_text)):
            self.__key_settings_rect.append(self.__key_settings_text[i].get_rect())
            self.__key_settings_rect[i].bottomleft = (
                screen_size[0] / 25,
                screen_size[1] * (5 / 7) + screen_size[1] * (1 / 3) * (i / 7),
            )

        return None

    @overrides
    def refresh(self) -> None:
        pygame.display.set_caption("Start")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN
        self.__screen = pygame.display.set_mode(
            self.__settings.get_screen_resolution(), flag
        )
        self.__menu_text = []
        self.__menu_rect = []
        self.__key_settings_text = []
        self.__key_settings_rect = []
        self.__selected_menu = 0
        self.__key = self.__settings.get_settings().get("key_settings")
        self.render()
        return None

    @overrides
    def draw(self) -> None:
        self.__screen.fill(colors.white)
        self.__screen.blit(self.__title_text, self.__title_rect)
        self.__selected_rect.center = self.__menu_rect[self.__selected_menu].center
        pygame.draw.rect(self.__screen, colors.black, self.__selected_rect, 2)
        for i in range(len(self.__menu_text)):
            self.__screen.blit(self.__menu_text[i], self.__menu_rect[i])
        for i in range(len(self.__key_settings_text)):
            self.__screen.blit(self.__key_settings_text[i], self.__key_settings_rect[i])

        return None

    @overrides
    def handle(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__menu_options)):
                if self.__menu_rect[i].collidepoint(mouse_pos):
                    self.__selected_menu = i
                    continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__menu_options)):
                if self.__menu_rect[i].collidepoint(mouse_pos):
                    self.sounds.play_effect("click")
                    return self.__menu_func(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == self.__key.get("up") or event.key == self.__key.get("left"):
                self.__selected_menu -= 1
                if self.__selected_menu < 0:
                    self.__selected_menu = len(self.__menu_options) - 1
            elif event.key == self.__key.get("down") or event.key == self.__key.get("right"):
                self.__selected_menu += 1
                if self.__selected_menu >= len(self.__menu_options):
                    self.__selected_menu = 0
            elif event.key == self.__key.get("select"):
                self.sounds.play_effect("click")
                return self.__menu_func(self.__selected_menu)
            elif event.key == self.__key.get("cancel"):
                return pygame.event.post(pygame.event.Event(pygame.QUIT))
        return ("continue", None)

    def __menu_func(self, i) -> None:
        if i == 0:  # Start
            self.__settings.previous_main()
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="gamelobby")
            )
        elif i == 1:  # Settings
            self.__settings.previous_main()
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="stage")
            )
        elif i == 2:  # Settings
            self.__settings.previous_main()
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="settings")
            )
        elif i == 3:  # Exit
            self.__settings.previous_none()
            return pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            print(self.__menu_options[i] + " clicked")
        return None
