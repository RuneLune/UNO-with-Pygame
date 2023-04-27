import pygame
from overrides import overrides
from typing import Final, List

import util.colors as colors
import event.events as events
from config.settings_function import Settings
from sound.sound import SoundManager
from scene.scene_old import Scene
from util.resource_manager import font_resource


class Settings_Scene(Scene):
    MAX_Inst: Final[int] = 1
    Inst_created: int = 0

    @overrides
    def __new__(cls, *args, **kwargs):
        if cls.Inst_created >= cls.MAX_Inst:
            raise ValueError("Cannot create more Settings Scene")
        cls.Inst_created += 1
        return super(Settings_Scene, cls).__new__(cls)

    @overrides
    def __init__(self, settings: Settings, sound_manager: SoundManager) -> None:
        self.__menu_options: List[str] = [
            "Screen Size |",
            "Fullscreen |",
            "Key Settings |",
            "Left |",
            "Right |",
            "Up |",
            "Down |",
            "Select |",
            "Cancel |",
            "Colorblind Mode |",
        ]
        self.__settings: Settings = settings
        self.sounds = sound_manager
        self.refresh()
        return None

    @overrides
    def render(self) -> None:
        settings = self.__settings.get_settings()
        screen_size = self.__settings.get_screen_resolution()

        self.__title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 10)
        )
        self.__menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 20)
        )

        self.__title_text = self.__title_font.render("Settings", True, colors.white)
        self.__title_rect = self.__title_text.get_rect()
        self.__title_rect.centerx = self.__screen.get_rect().centerx
        self.__title_rect.bottom = self.__screen.get_rect().centery / 4

        for i in range(len(self.__menu_options)):
            self.__menu_text.append(
                self.__menu_font.render(self.__menu_options[i], True, colors.white)
            )
            self.__menu_rect.append(self.__menu_text[i].get_rect())
            self.__menu_rect[i].right = self.__screen.get_rect().centerx * 0.9
            self.__menu_rect[i].top = (
                self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
            )
            if i == 0:  # Screen Size
                self.__setting_text.append(
                    self.__menu_font.render(
                        settings.get("screen_size", None), True, colors.white
                    )
                )
                self.__button_text.append(
                    self.__menu_font.render("◀", True, colors.white)
                )
                self.__button_rect.append(self.__button_text[-1].get_rect())
                self.__button_rect[-1].left = self.__screen.get_rect().centerx
                self.__button_rect[-1].top = (
                    self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
                )
                self.__button_text.append(
                    self.__menu_font.render("▶", True, colors.white)
                )
                self.__button_rect.append(self.__button_text[-1].get_rect())
                self.__button_rect[-1].right = self.__screen.get_rect().centerx * 1.5
                self.__button_rect[-1].top = (
                    self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
                )
            elif i == 1:  # Fullscreen
                if settings.get("fullscreen", None) is True:
                    text = "Enable"
                else:
                    text = "Disable"
                self.__setting_text.append(
                    self.__menu_font.render(text, True, colors.white)
                )
                self.__button_text.append(
                    self.__menu_font.render("◀", True, colors.white)
                )
                self.__button_rect.append(self.__button_text[-1].get_rect())
                self.__button_rect[-1].left = self.__screen.get_rect().centerx
                self.__button_rect[-1].top = (
                    self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
                )
                self.__button_text.append(
                    self.__menu_font.render("▶", True, colors.white)
                )
                self.__button_rect.append(self.__button_text[-1].get_rect())
                self.__button_rect[-1].right = self.__screen.get_rect().centerx * 1.5
                self.__button_rect[-1].top = (
                    self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
                )
            elif i == 3:  # Key Settings - Left
                self.__setting_text.append(
                    self.__menu_font.render(
                        pygame.key.name(
                            settings.get("key_settings", None).get("left", None)
                        ),
                        True,
                        colors.white,
                    )
                )
            elif i == 4:  # Key Settings - Right
                self.__setting_text.append(
                    self.__menu_font.render(
                        pygame.key.name(
                            settings.get("key_settings", None).get("right", None)
                        ),
                        True,
                        colors.white,
                    )
                )
            elif i == 5:  # Key Settings - Up
                self.__setting_text.append(
                    self.__menu_font.render(
                        pygame.key.name(
                            settings.get("key_settings", None).get("up", None)
                        ),
                        True,
                        colors.white,
                    )
                )
            elif i == 6:  # Key Settings - Down
                self.__setting_text.append(
                    self.__menu_font.render(
                        pygame.key.name(
                            settings.get("key_settings", None).get("down", None)
                        ),
                        True,
                        colors.white,
                    )
                )
            elif i == 7:  # Key Settings - Select
                self.__setting_text.append(
                    self.__menu_font.render(
                        pygame.key.name(
                            settings.get("key_settings", None).get("select", None)
                        ),
                        True,
                        colors.white,
                    )
                )
            elif i == 8:  # Key Settings - Cancel
                self.__setting_text.append(
                    self.__menu_font.render(
                        pygame.key.name(
                            settings.get("key_settings", None).get("cancel", None)
                        ),
                        True,
                        colors.white,
                    )
                )
            elif i == 9:  # Colorblind Mode
                if settings.get("colorblind_mode", None) is True:
                    text = "Enable"
                else:
                    text = "Disable"
                self.__setting_text.append(
                    self.__menu_font.render(text, True, colors.white)
                )
                self.__button_text.append(
                    self.__menu_font.render("◀", True, colors.white)
                )
                self.__button_rect.append(self.__button_text[-1].get_rect())
                self.__button_rect[-1].left = self.__screen.get_rect().centerx
                self.__button_rect[-1].top = (
                    self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
                )
                self.__button_text.append(
                    self.__menu_font.render("▶", True, colors.white)
                )
                self.__button_rect.append(self.__button_text[-1].get_rect())
                self.__button_rect[-1].right = self.__screen.get_rect().centerx * 1.5
                self.__button_rect[-1].top = (
                    self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
                )
            else:
                self.__setting_text.append(
                    self.__menu_font.render("", True, colors.white)
                )
            self.__setting_rect.append(self.__setting_text[i].get_rect())
            self.__setting_rect[i].centerx = self.__screen.get_rect().centerx * 1.25
            self.__setting_rect[i].top = (
                self.__screen.get_rect().centery / 3 + i * screen_size[1] / 16
            )
        # 뒤로 가기 버튼 추가
        self.__button_text.append(self.__menu_font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[-1].bottom = self.__screen.get_rect().centery / 5

        # Default Settings
        self.__button_text.append(
            self.__menu_font.render("Reset to Default Settings", True, colors.white)
        )
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx
        self.__button_rect[-1].top = (
            self.__screen.get_rect().centery / 3 + 10 * screen_size[1] / 16
        )

        # 소리 조절 버튼
        self.__background_sound_text = self.__menu_font.render(
            "BGM", True, colors.white
        )
        self.__background_sound_text_rect = self.__background_sound_text.get_rect()
        self.__background_sound_text_rect.centerx = (
            self.__screen.get_rect().centerx * 1.5 + 100
        )
        self.__background_sound_text_rect.top = self.__screen.get_rect().bottom / 2.7

        self.__button_text.append(self.__menu_font.render("▲", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx * 1.5 + 100
        self.__button_rect[-1].top = self.__screen.get_rect().bottom / 2.39

        self.__sound_setting_text.append(
            self.__menu_font.render(
                str(settings.get("background_sound_volume", None)), True, colors.white
            )
        )
        self.__sound_setting_text_rect.append(self.__sound_setting_text[-1].get_rect())
        self.__sound_setting_text_rect[-1].centerx = (
            self.__screen.get_rect().centerx * 1.5 + 100
        )
        self.__sound_setting_text_rect[-1].top = self.__screen.get_rect().bottom / 2.1

        self.__button_text.append(self.__menu_font.render("▼", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx * 1.5 + 100
        self.__button_rect[-1].top = self.__screen.get_rect().bottom / 1.9

        self.__effect_sound_text = self.__menu_font.render("EFF", True, colors.white)
        self.__effect_sound_text_rect = self.__effect_sound_text.get_rect()
        self.__effect_sound_text_rect.centerx = (
            self.__screen.get_rect().centerx * 1.5 + 100
        )
        self.__effect_sound_text_rect.top = self.__screen.get_rect().bottom / 1.7

        self.__button_text.append(self.__menu_font.render("▲", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx * 1.5 + 100
        self.__button_rect[-1].top = self.__screen.get_rect().bottom / 1.56

        self.__sound_setting_text.append(
            self.__menu_font.render(
                str(settings.get("effect_sound_volume", None)), False, colors.white
            )
        )
        self.__sound_setting_text_rect.append(self.__sound_setting_text[-1].get_rect())
        self.__sound_setting_text_rect[-1].centerx = (
            self.__screen.get_rect().centerx * 1.5 + 100
        )
        self.__sound_setting_text_rect[-1].top = self.__screen.get_rect().bottom / 1.44

        self.__button_text.append(self.__menu_font.render("▼", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx * 1.5 + 100
        self.__button_rect[-1].top = self.__screen.get_rect().bottom / 1.34

        self.__all_sound_text = self.__menu_font.render("ALL", True, colors.white)
        self.__all_sound_text_rect = self.__all_sound_text.get_rect()
        self.__all_sound_text_rect.centerx = (
            self.__screen.get_rect().centerx * 1.5 + 100
        )
        self.__all_sound_text_rect.top = self.__screen.get_rect().centery / 4

        self.__button_text.append(self.__menu_font.render("▲", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx * 1.5 + 100
        self.__button_rect[-1].top = self.__screen.get_rect().centery / 2.8

        self.__sound_setting_text.append(
            self.__menu_font.render(
                str(settings.get("all_sound_volume", None)), False, colors.white
            )
        )
        self.__sound_setting_text_rect.append(self.__sound_setting_text[-1].get_rect())
        self.__sound_setting_text_rect[-1].centerx = (
            self.__screen.get_rect().centerx * 1.5 + 100
        )
        self.__sound_setting_text_rect[-1].top = self.__screen.get_rect().centery / 2.1

        self.__button_text.append(self.__menu_font.render("▼", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].centerx = self.__screen.get_rect().centerx * 1.5 + 100
        self.__button_rect[-1].top = self.__screen.get_rect().centery / 1.7

        # 메인 메뉴 돌아가기 버튼 추가
        if (
            settings.get("previous_scene", None) != "main"
        ):  # if previous scene is not main
            self.__button_text.append(
                self.__title_font.render("Back to Main menu", True, colors.white)
            )
            self.__button_rect.append(self.__button_text[-1].get_rect())
            self.__button_rect[-1].centerx = self.__screen.get_rect().centerx
            self.__title_rect.bottom = self.__screen.get_rect().centery / 4
            self.__button_rect[-1].top = self.__screen.get_rect().centery * 7 / 4

        # 키 종류별 선택 버튼 추가

        return None

    @overrides
    def refresh(self) -> None:
        pygame.display.set_caption("Settings")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN
        self.__screen = pygame.display.set_mode(
            self.__settings.get_screen_resolution(), flag
        )
        self.__menu_text = []
        self.__menu_rect = []
        self.__setting_text = []
        self.__setting_rect = []
        self.__button_text = []
        self.__button_rect = []
        self.__sound_setting_text = []
        self.__sound_setting_text_rect = []
        self.render()
        return None

    @overrides
    def draw(self) -> None:
        self.__screen.fill(colors.black)
        # Setting Scene 제목 출력
        self.__screen.blit(self.__title_text, self.__title_rect)
        # 세팅 메뉴 출력
        for i in range(len(self.__menu_text)):
            self.__screen.blit(self.__menu_text[i], self.__menu_rect[i])
        # 현 세팅 출력 (세팅 메뉴 옆)
        for i in range(len(self.__setting_text)):
            self.__screen.blit(self.__setting_text[i], self.__setting_rect[i])

        # 버튼 출력
        for i in range(len(self.__button_text)):
            self.__screen.blit(self.__button_text[i], self.__button_rect[i])

        # 사운드 버튼 출력
        self.__screen.blit(
            self.__background_sound_text, self.__background_sound_text_rect
        )
        self.__screen.blit(self.__effect_sound_text, self.__effect_sound_text_rect)
        self.__screen.blit(self.__all_sound_text, self.__all_sound_text_rect)

        for i in range(len(self.__sound_setting_text)):
            self.__screen.blit(
                self.__sound_setting_text[i], self.__sound_setting_text_rect[i]
            )

        return None

    @overrides
    def handle(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_text)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    self.sounds.play_effect("click")
                    return self.__button_func(i)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__setting_rect)):
                if self.__setting_rect[i].collidepoint(mouse_pos):
                    self.sounds.play_effect("click")
                    return self.__setting_func(i)
        if event.type == pygame.KEYDOWN:
            if event.key == self.__settings.get_settings().get("key_settings").get("cancel"):
                return pygame.event.post(
                    pygame.event.Event(
                        events.CHANGE_SCENE,
                        target=self.__settings.get_settings().get(
                            "previous_scene", None
                        ),
                    )
                )

        return "continue"

    def __button_func(self, i):
        if self.__settings.get_settings().get("fullscreen", False) is False:
            if i == 0:  # Lower Screen Resolution
                self.__settings.lower_screen_size()
            elif i == 1:  # Higher Screen Resolution
                self.__settings.higher_screen_size()
        if i == 2 or i == 3:  # Change Fullscreen Option
            self.__settings.change_fullscreen()
        elif i == 4 or i == 5:  # Change Colorblind Mode Option
            self.__settings.change_colorblind_mode()
        elif i == 6:  # Back
            # if previous scene is main
            if self.__settings.get_settings().get("previous_scene") == "main":
                return pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="main")
                )
            # if previous scene is game
            elif self.__settings.get_settings().get("previous_scene") == "gameui":
                return pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="gameui")
                )
        elif i == 7:  # Default Settings
            self.__settings.reset_settings()
            self.__settings.set_screen_resolution()
        elif i == 8:
            self.__settings.higher_background_sound_volume()
        elif i == 9:
            self.__settings.lower_background_sound_volume()
        elif i == 10:
            self.__settings.higher_effect_sound_volume()
        elif i == 11:
            self.__settings.lower_effect_sound_volume()
        elif i == 12:
            self.__settings.higher_all_sound_volume()
        elif i == 13:
            self.__settings.lower_all_sound_volume()
        elif i == 14:  # Back to Main menu
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="main")
            )
        ##################
        # 키 종류별 인덱스 추가 후 커스텀 함수 실행 및 결과 저장
        pygame.event.post(pygame.event.Event(events.CHANGE_SETTINGS))
        return None

    def __setting_func(self, i):
        if i == 3:
            left_text = self.__menu_font.render(
                pygame.key.name(
                    self.__settings.get_settings()
                    .get("key_settings", None)
                    .get("left", None)
                ),
                True,
                colors.red,
            )
            self.__screen.blit(left_text, self.__setting_rect[i])
            pygame.display.update()
            left = self.__settings.key_change()
            self.__settings.set_key_value("left", left)
        elif i == 4:
            right_text = self.__menu_font.render(
                pygame.key.name(
                    self.__settings.get_settings()
                    .get("key_settings", None)
                    .get("right", None)
                ),
                True,
                colors.red,
            )
            self.__screen.blit(right_text, self.__setting_rect[i])
            pygame.display.update()
            right = self.__settings.key_change()
            self.__settings.set_key_value("right", right)
        elif i == 5:
            up_text = self.__menu_font.render(
                pygame.key.name(
                    self.__settings.get_settings()
                    .get("key_settings", None)
                    .get("up", None)
                ),
                True,
                colors.red,
            )
            self.__screen.blit(up_text, self.__setting_rect[i])
            pygame.display.update()
            up = self.__settings.key_change()
            self.__settings.set_key_value("up", up)
        elif i == 6:
            down_text = self.__menu_font.render(
                pygame.key.name(
                    self.__settings.get_settings()
                    .get("key_settings", None)
                    .get("down", None)
                ),
                True,
                colors.red,
            )
            self.__screen.blit(down_text, self.__setting_rect[i])
            pygame.display.update()
            down = self.__settings.key_change()
            self.__settings.set_key_value("down", down)
        elif i == 7:
            select_text = self.__menu_font.render(
                pygame.key.name(
                    self.__settings.get_settings()
                    .get("key_settings", None)
                    .get("select", None)
                ),
                True,
                colors.red,
            )
            self.__screen.blit(select_text, self.__setting_rect[i])
            pygame.display.update()
            select = self.__settings.key_change()
            self.__settings.set_key_value("select", select)
        elif i == 8:
            cancel_text = self.__menu_font.render(
                pygame.key.name(
                    self.__settings.get_settings()
                    .get("key_settings", None)
                    .get("cancel", None)
                ),
                True,
                colors.red,
            )
            self.__screen.blit(cancel_text, self.__setting_rect[i])
            pygame.display.update()
            cancel = self.__settings.key_change()
            self.__settings.set_key_value("cancel", cancel)

        pygame.event.post(pygame.event.Event(events.CHANGE_SETTINGS))
        return None
