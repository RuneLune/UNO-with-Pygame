import pygame

import colors
import events


class Settings_Scene:
    MAX_Inst = 1
    Inst_created = 0

    def __new__(cls, *args, **kwargs):
        if cls.Inst_created >= cls.MAX_Inst:
            raise ValueError("Cannot create more Settings Scene")
        cls.Inst_created += 1
        return super().__new__(cls)

    def __init__(self, settings):
        self.__menu_options = [
            "Screen Size |",
            "Fullscreen |",
            "Key Settings |",
            "Up |",
            "Down |",
            "Left |",
            "Right |",
            "Select |",
            "Cancel |",
            "Colorblind Mode |",
        ]
        self.__settings = settings
        self.refresh()
        return super().__init__()

    def render(self):
        settings = self.__settings.get_settings()
        screen_size = self.__settings.get_screen_resolution()

        self.__title_font = pygame.font.Font(
            "res/font/MainFont.ttf", round(screen_size[1] / 10)
        )
        self.__menu_font = pygame.font.Font(
            "res/font/MainFont.ttf", round(screen_size[1] / 20)
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
        self.__button_text.append(self.__menu_font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[-1].bottom = self.__screen.get_rect().centery / 5
        return None

    def refresh(self):
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
        self.render()
        return None

    def draw(self):
        self.__screen.fill(colors.black)
        self.__screen.blit(self.__title_text, self.__title_rect)
        for i in range(len(self.__menu_text)):
            self.__screen.blit(self.__menu_text[i], self.__menu_rect[i])
        for i in range(len(self.__setting_text)):
            self.__screen.blit(self.__setting_text[i], self.__setting_rect[i])
        for i in range(len(self.__button_text)):
            self.__screen.blit(self.__button_text[i], self.__button_rect[i])

        return None

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_text)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    return self.__button_func(i)

        return "continue"

    def __menu_func(self, i):
        if i == 0:  # Back
            return ("scene", "main")
        else:
            print(self.__menu_options[i] + " clicked")
        return ("continue", None)

    def __button_func(self, i):
        if self.__settings.get_settings().get("fullscreen", False) is False:
            if i == 0:  # Lower Screen Resolution
                self.__settings.lower_screen_size()
            elif i == 1:  # Higher Screen Resolution
                self.__settings.higher_screen_size()
        if i == 2 or i == 3:  # Change Fullscreen Option
            self.__settings.change_fullscreen()
        if i == 4 or i == 5:  # Change Colorblind Mode Option
            self.__settings.change_colorblind_mode()
        elif i == 6:  # Back to main
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="main")
            )
        self.refresh()
        return None
