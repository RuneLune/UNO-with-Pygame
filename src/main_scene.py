import pygame

import colors
import events


class Main_Scene:
    MAX_Inst = 1
    Inst_created = 0

    def __new__(cls, *args, **kwargs):
        if cls.Inst_created >= cls.MAX_Inst:
            raise ValueError("Cannot create more Main Scene")
        cls.Inst_created += 1
        return super().__new__(cls)

    def __init__(self, settings):
        self.__menu_options = ["Start", "Story", "Settings", "Quit"]
        self.__settings = settings
        self.refresh()
        return super().__init__()

    def render(self):
        screen_size = self.__settings.get_screen_resolution()

        self.__title_font = pygame.font.Font(
            "res/font/MainFont.ttf", round(screen_size[1] / 3)
        )
        self.__menu_font = pygame.font.Font(
            "res/font/MainFont.ttf",
            round(screen_size[1] / (3.3 * len(self.__menu_options))),
        )

        self.__title_text = self.__title_font.render("UNO", True, colors.black)
        self.__title_rect = self.__title_text.get_rect()
        self.__title_rect.centerx = self.__screen.get_rect().centerx
        self.__title_rect.bottom = self.__screen.get_rect().centery

        for i in range(len(self.__menu_options)):
            self.__menu_text.append(self.__menu_font.render(self.__menu_options[i], True, colors.black))
            self.__menu_rect.append(self.__menu_text[i].get_rect())
            self.__menu_rect[i].centerx = self.__screen.get_rect().centerx
            self.__menu_rect[i].top = self.__screen.get_rect().centery + i * screen_size[1] / (3 * len(self.__menu_options))
        self.__selected_rect = pygame.Rect(0, 0, screen_size[0] / 3, screen_size[1] / (3 * len(self.__menu_options)))
        return None

    def refresh(self):
        pygame.display.set_caption("Start")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN
        self.__screen = pygame.display.set_mode(
            self.__settings.get_screen_resolution(), flag
        )
        self.__menu_text = []
        self.__menu_rect = []
        self.__selected_menu = 0
        self.render()
        return None

    def draw(self):
        self.__screen.fill(colors.white)
        self.__screen.blit(self.__title_text, self.__title_rect)
        self.__selected_rect.center = self.__menu_rect[self.__selected_menu].center
        pygame.draw.rect(self.__screen, colors.black, self.__selected_rect, 2)
        for i in range(len(self.__menu_text)):
            self.__screen.blit(self.__menu_text[i], self.__menu_rect[i])

        return None

    def handle(self, event):
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
                    return self.__menu_func(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.__selected_menu -= 1
                if self.__selected_menu < 0:
                    self.__selected_menu = len(self.__menu_options) - 1
            elif event.key == pygame.K_DOWN:
                self.__selected_menu += 1
                if self.__selected_menu >= len(self.__menu_options):
                    self.__selected_menu = 0
            elif event.key == pygame.K_RETURN:
                return self.__menu_func(self.__selected_menu)
            elif event.key == pygame.K_ESCAPE:
                return pygame.event.post(pygame.event.Event(pygame.QUIT))
        return ("continue", None)

    def __menu_func(self, i):
        if i == 0:  # Start
            self.__settings.get_real_settings().update(previous_scene="main")
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="gameui"))
        elif i == 1:  # Settings
            self.__settings.get_real_settings().update(previous_scene="main")
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="stage"))
        elif i == 2:  # Settings
            self.__settings.get_real_settings().update(previous_scene="main")
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="settings"))
        elif i == 3:  # Exit
            self.__settings.get_real_settings().update(previous_scene=None)
            return pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            print(self.__menu_options[i] + " clicked")
        return None