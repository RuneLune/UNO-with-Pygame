import pygame
from overrides import overrides
from os.path import join

import copy
import json
import os

import colors
import events
from sound import SoundManager
from scene import Scene
from resource_manager import font_resource, image_resource
from settings_function import Settings
from stage_a import Stage_A
from stage_b import Stage_B
from stage_c import Stage_C
from stage_d import Stage_D


initial_settings = {"touchable": [True, True, False, False, False]}


class Stage(Scene):
    @overrides
    def __init__(self, settings: Settings, sound_manager: SoundManager) -> None:
        self.__stage_num = 4
        self.__settings = settings
        self.__is_confirm = False
        global initial_settings
        self.__stage_states = initial_settings

        # Create settings.json if not exist
        if not os.path.isfile("stage_states.json"):
            self.reset_stage_stages()
            self.save_stage_states()
        else:
            self.load_stage_states()

        self.sounds = sound_manager
        self.refresh()

        return None

    # Settings load method
    def load_stage_states(self):
        # load saved settings from file
        if os.path.isfile("stage_states.json"):
            try:
                with open("stage_states.json", "r") as f:
                    self.__stage_states = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass

    # Settings reset method
    def reset_stage_stages(self):
        global initial_settings
        self.__stage_states = copy.deepcopy(initial_settings)

    # Settings save method
    def save_stage_states(self):
        try:
            # Save settings to file
            with open("stage_states.json", "w") as f:
                json.dump(self.__stage_states, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load_stage_states()
        # Return 0 if save was successful
        return 0

    def get_stage_states(self):
        return copy.deepcopy(self.__stage_states)

    @overrides
    def render(self) -> None:
        # screen size
        screen_size = self.__settings.get_screen_resolution()
        self.surface = pygame.Surface(screen_size)

        # font
        self.__title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 6)
        )
        self.__back_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 20)
        )
        self.__imformation_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 30)
        )
        self.__window_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 15)
        )

        # title
        self.__title_text = self.__title_font.render("STAGE", True, colors.white)
        self.__title_rect = self.__title_text.get_rect()
        self.__title_rect.centerx = self.__screen.get_rect().centerx
        self.__title_rect.bottom = self.__screen.get_rect().centery / 2

        # back button
        self.__button_text.append(self.__back_font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[0].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[0].bottom = self.__screen.get_rect().centery / 5

        # 게임 정보
        for i in range(len(self.__imformation)):
            self.__imformation_text.append(
                self.__imformation_font.render(
                    self.__imformation[i], True, colors.white
                )
            )
        self.__imformation_rect = self.__imformation_text[-1].get_rect()
        self.__imformation_rect.top = self.__screen.get_rect().centery + 70
        self.__imformation_rect.left = self.__screen.get_rect().right / 10

        # stage
        # 1번 인덱스는 back에 관련된 것이므로 1번부터 슬라이싱
        self.button_rects = self.__touchable[1:]
        for i in range(self.__stage_num):
            if self.button_rects[i]:
                image = pygame.image.load(
                    image_resource(join("stage", f"stage_{i+1}.png"))
                )
            else:
                image = pygame.image.load(image_resource(join("stage", "stage_0.png")))
            self.__stage_img.append(image)
            self.__button_rect.append(self.__stage_img[i].get_rect())
            self.__button_rect[i + 1].centery = self.__screen.get_rect().centery
            if i == 0:
                self.__button_rect[i + 1].left = self.__screen.get_rect().right / 10
            elif i == 1:
                self.__button_rect[i + 1].left = self.__screen.get_rect().right / 3.5
            elif i == 2:
                self.__button_rect[i + 1].left = self.__screen.get_rect().right / 2
            elif i == 3:
                self.__button_rect[i + 1].right = self.__screen.get_rect().right / 1.2

        # window
        self.__window_text = self.__window_font.render(
            "Do you want to start?", True, colors.black
        )
        self.__window_text_rect = self.__window_text.get_rect()
        self.__window_text_rect.top = self.__screen.get_rect().centery + 110
        self.__window_text_rect.center = self.__screen.get_rect().center

        self.__window_img.append(
            pygame.image.load(image_resource(join("stage", "yes.png")))
        )
        self.__window_img.append(
            pygame.image.load(image_resource(join("stage", "no.png")))
        )
        self.__window_rect.append(self.__window_img[0].get_rect())
        self.__window_rect.append(self.__window_img[1].get_rect())
        for i in range(len(self.__window_rect)):
            self.__window_rect[i].top = self.__screen.get_rect().centery + 200
            if i == 0:
                self.__window_rect[i].left = self.__screen.get_rect().right / 10
            elif i == 1:
                self.__window_rect[i].right = self.__screen.get_rect().right / 1.2

        self.__background = pygame.Surface(
            (self.__screen.get_width(), self.__screen.get_height())
        )
        self.__background.fill((255, 255, 255))
        self.__background.set_alpha(200)

        # 하이라이트
        self.__selected_rect = pygame.Rect(0, 0, 130, 130)
        self.__selected_window_rect = pygame.Rect(0, 0, 130, 110)

        return None

    @overrides
    def refresh(self) -> None:
        pygame.display.set_caption("STAGE")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN
        self.__screen = pygame.display.set_mode(
            self.__settings.get_screen_resolution(), flag
        )
        self.__button_text = []
        self.__button_rect = []
        self.__stage_img = []
        self.__window_img = []
        self.__imformation_text = []
        self.__imformation = [
            "첫 분배 시 컴퓨터 플레이어에게 기술 카드를 50% 더 높은 확률로 분배",
            "3명의 컴퓨터 플레이어와 대전 / 첫 분배 시 모든 카드를 같은 수로 분배 (첫 카드 제외)",
            "2명의 컴퓨터 플레이어와 대전 / 매 5턴마다 낼 수 있는 카드 색상 무작위 변경",
            "유저 드로우 시 1장이 아닌 2장 드로우",
        ]
        # 첫번쨰 인덱스는 back 버튼을 위한 것. 2~5가 스테이지를 위한 엘리먼트들
        self.__touchable = self.get_stage_states().get("touchable")
        self.__window_rect = []
        self.__selected_stage = 0
        self.__selected_window = 0
        self.render()
        return None

    @overrides
    def draw(self) -> None:
        self.__screen.fill(colors.black)

        # title
        self.__screen.blit(self.__title_text, self.__title_rect)

        # back button
        self.__screen.blit(self.__button_text[0], self.__button_rect[0])

        # stage
        for i, img in enumerate(self.__stage_img):
            self.__screen.blit(img, self.__button_rect[i + 1])

        # hover
        if self.__selected_stage != 0:
            # 첫 번째 메뉴 옵션을 제외한 나머지 메뉴 옵션 정보를 가져옴
            button_rects = self.__button_rect[1:]
            # 현재 선택된 메뉴 옵션의 위치와 크기 정보를 저장하는 객체
            selected_rect = pygame.Rect(
                0, 0, self.__selected_rect.width, self.__selected_rect.height
            )
            # 선택된 메뉴 옵션의 위치와 크기 정보를 현재 선택된 메뉴 옵션의 위치와 크기 정보로 설정
            selected_rect.center = button_rects[self.__selected_stage - 1].center
            # 화면에 선택된 메뉴 옵션에 흰색 테두리를 그림
            pygame.draw.rect(self.__screen, colors.white, selected_rect, 2)
            self.__screen.blit(
                self.__imformation_text[self.__selected_stage - 1],
                self.__imformation_rect,
            )

        if self.__is_confirm:
            self.draw_window()

        return None

    def draw_window(self):
        self.__screen.blit(self.__background, (0, 0))

        self.__screen.blit(self.__window_text, self.__window_text_rect)

        for i, img in enumerate(self.__window_img):
            self.__screen.blit(img, self.__window_rect[i])

        selected_window_rect = pygame.Rect(
            0, 0, self.__selected_window_rect.width, self.__selected_window_rect.height
        )
        selected_window_rect.center = self.__window_rect[self.__selected_window].center
        pygame.draw.rect(self.__screen, colors.white, selected_window_rect, 2)

    @overrides
    def handle(self, event: pygame.event.Event):
        if event.type == events.GAME_END:
            if (
                hasattr(event, "args")
                and "stage" in event.args
                and "status" in event.args
            ):
                if event.args.get("status") == "win":
                    if event.args.get("stage") == "stage_a":
                        self.__stage_states["touchable"][2] = True
                        self.save_stage_states()
                        pass
                    elif event.args.get("stage") == "stage_b":
                        self.__stage_states["touchable"][3] = True
                        self.save_stage_states()
                        pass
                    elif event.args.get("stage") == "stage_c":
                        self.__stage_states["touchable"][4] = True
                        self.save_stage_states()
                        pass
                    pass
                pass

            pass
        if self.__is_confirm is False:
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(self.__button_rect)):
                    if self.__touchable[i] and self.__button_rect[i].collidepoint(
                        mouse_pos
                    ):
                        self.__selected_stage = i
                        continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(self.__button_rect)):
                    if self.__touchable[i] and self.__button_rect[i].collidepoint(
                        mouse_pos
                    ):
                        self.sounds.play_effect("click")
                        return self.__menu_func(i)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__selected_stage -= 1
                    if self.__selected_stage < 0:
                        self.__selected_stage = len(self.__button_rect) - 1
                    while not self.__touchable[self.__selected_stage]:
                        self.__selected_stage -= 1
                        if self.__selected_stage < 0:
                            self.__selected_stage = len(self.__button_rect) - 1
                elif event.key == pygame.K_RIGHT:
                    self.__selected_stage += 1
                    if self.__selected_stage >= len(self.__button_rect):
                        self.__selected_stage = 0
                    while not self.__touchable[self.__selected_stage]:
                        self.__selected_stage += 1
                        if self.__selected_stage >= len(self.__button_rect):
                            self.__selected_stage = 0
                elif event.key == pygame.K_RETURN:
                    self.sounds.play_effect("click")
                    return self.__menu_func(self.__selected_stage)
                elif event.key == pygame.K_ESCAPE:
                    return pygame.event.post(
                        pygame.event.Event(events.CHANGE_SCENE, target="main")
                    )
        else:
            self.__window_handle(event, self.__selected_stage)

        return None

    def __window_handle(self, event, idx):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__window_rect)):
                if self.__window_rect[i].collidepoint(mouse_pos):
                    self.__selected_window = i
                    continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__window_rect)):
                if self.__window_rect[i].collidepoint(mouse_pos):
                    self.sounds.play_effect("click")
                    return self.__window_func(i, idx)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.__selected_window -= 1
                if self.__selected_window < 0:
                    self.__selected_window = len(self.__window_rect) - 1
            elif event.key == pygame.K_RIGHT:
                self.__selected_window += 1
                if self.__selected_window >= len(self.__window_rect):
                    self.__selected_window = 0
            elif event.key == pygame.K_RETURN:
                self.sounds.play_effect("click")
                return self.__window_func(self.__selected_window, idx)

    def __menu_func(self, i):
        if i == 0:
            self.__settings.previous_stageselect()
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="main")
            )
        elif i == 1 or i == 2 or i == 3 or i == 4:
            self.__is_confirm = True
            pass

    def __window_func(self, i, idx):
        if i == 0:
            if idx == 1:
                self.__is_confirm = False
                return pygame.event.post(
                    pygame.event.Event(
                        events.CHANGE_SCENE,
                        target="gameui",
                        args={"game": Stage_A()},
                    )
                )
            elif idx == 2:
                self.__is_confirm = False
                return pygame.event.post(
                    pygame.event.Event(
                        events.CHANGE_SCENE,
                        target="gameui",
                        args={"game": Stage_B()},
                    )
                )
            elif idx == 3:
                self.__is_confirm = False
                return pygame.event.post(
                    pygame.event.Event(
                        events.CHANGE_SCENE,
                        target="gameui",
                        args={"game": Stage_C()},
                    )
                )
            elif idx == 4:
                self.__is_confirm = False
                return pygame.event.post(
                    pygame.event.Event(
                        events.CHANGE_SCENE,
                        target="gameui",
                        args={"game": Stage_D()},
                    )
                )

        else:
            self.__is_confirm = False
