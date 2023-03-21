import pygame

import colors
import events


class Start_Scene:
    MAX_Inst = 1
    Inst_created = 0

    def __new__(cls, *args, **kwargs):
        if cls.Inst_created >= cls.MAX_Inst:
            raise ValueError("Cannot create more Start Scene")
        cls.Inst_created += 1
        return super().__new__(cls)

    def __init__(self, settings):
        self.__menu_options = ["Back to main menu"]
        self.__settings = settings
        self.refresh()
        return super().__init__()

    def render(self):
        screen_size = self.__settings.get_screen_resolution()

        self.__title_font = pygame.font.Font(
            "res/font/MainFont.ttf", round(screen_size[1] / 10)
        )
        self.__menu_font = pygame.font.Font(
            "res/font/MainFont.ttf", round(screen_size[1] / 20)
        )

        self.__title_text = self.__title_font.render("Start Scene", True, colors.white)
        self.__title_rect = self.__title_text.get_rect()
        self.__title_rect.centerx = self.__screen.get_rect().centerx
        self.__title_rect.bottom = self.__screen.get_rect().centery

        for i in range(len(self.__menu_options)):
            self.__menu_text.append(
                self.__menu_font.render(self.__menu_options[i], True, colors.white)
            )
            self.__menu_rect.append(self.__menu_text[i].get_rect())
            self.__menu_rect[i].centerx = self.__screen.get_rect().centerx
            self.__menu_rect[
                i
            ].top = self.__screen.get_rect().centery + i * screen_size[1] / (
                3 * len(self.__menu_options)
            )
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
        self.render()
        return None

    def draw(self):
        self.__screen.fill(colors.black)
        self.__screen.blit(self.__title_text, self.__title_rect)
        for i in range(len(self.__menu_text)):
            self.__screen.blit(self.__menu_text[i], self.__menu_rect[i])

        return None

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__menu_text)):
                if self.__menu_rect[i].collidepoint(mouse_pos):
                    return self.__menu_func(i)

        return "continue"

    def __menu_func(self, i):
        if i == 0:  # Back
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="main"))
        else:
            print(self.__menu_options[i] + " clicked")
        return None
