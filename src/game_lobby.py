import pygame
import colors
import events
from overrides import overrides

import copy
import json
import os

from resource_manager import font_resource
from scene import Scene
from game import Game
from settings_function import Settings
from sound import SoundManager

initial_settings = {
    "player_count": 2,
    "pressed_bots": {
        "bot1": False,
        "bot2": True,
        "bot3": True,
        "bot4": True,
        "bot5": True
    },
    "user_name": " User_Name (Press Enter)"
}

class Game_Lobby(Scene):
    @overrides
    def __init__(self, settings: Settings, sound_manager: SoundManager):
        # self.game = Game(6) # 임시 플레이어 수
        self.__settings = settings

        # Create settings.json if not exist
        if not os.path.isfile("game_settings.json"):
            self.reset_game_settings()
            self.save_game_settings()
        else:
            self.load_game_settings()

        self.sounds = sound_manager
        self.refresh()

        # load user and bot object
        # self.players = self.game.get_players()
        self.bots = []

        return None

    # Settings load method
    def load_game_settings(self):
        # load saved settings from file
        if os.path.isfile("game_settings.json"):
            try:
                with open("game_settings.json", "r") as f:
                    self.__game_settings = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass
    
    # Settings reset method
    def reset_game_settings(self):
        global initial_settings
        self.__game_settings = copy.deepcopy(initial_settings)

    # Settings save method
    def save_game_settings(self):
        try:
            # Save settings to file
            with open("game_settings.json", "w") as f:
                json.dump(self.__game_settings, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load_game_settings()
        # Return 0 if save was successful
        return 0
    
    def get_game_settings(self):
        return copy.deepcopy(self.__game_settings)

    @overrides
    def render(self):
        # 스크린 사이즈
        screen_size = self.__settings.get_screen_resolution()
        self.surface = pygame.Surface(screen_size)

        # 폰트 생성
        self.__game_font = pygame.font.Font(
            font_resource("Travel.ttf"), round(screen_size[1] / 15)
        )
        self.__back_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 20)
        )
        self.__start_font = pygame.font.Font(
            font_resource("MainFont.ttf"), round(screen_size[1] / 10)
        )

        # 덱/유저/봇 공간 사이즈와 위치 정의
        deck_space_size = (screen_size[0] * (3 / 4), screen_size[1] * (2 / 3))
        deck_space_pos = (0, 0)

        user_space_size = (screen_size[0] * (3 / 4), screen_size[1] * (1 / 3))
        self.user_space_pos = (0, deck_space_size[1])

        self.bots_space_size = (screen_size[0] * (1 / 4), screen_size[1] * (1 / 5))
        self.bots_space_pos = [
            (user_space_size[0], i * self.bots_space_size[1]) for i in range(0, 5)
        ]

        # 공간 사각형 정의
        self.deck_space = pygame.Rect(deck_space_pos, deck_space_size)
        self.user_space = pygame.Rect(self.user_space_pos, user_space_size)
        self.bots_space = [
            pygame.Rect(self.bots_space_pos[i], self.bots_space_size)
            for i in range(0, 5)
        ]

        # 뒤로가기 버튼 추가
        self.__button_text.append(self.__back_font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[-1].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[-1].bottom = self.__screen.get_rect().centery / 5

        # 스타트 버튼 추가 및 스타트 버튼 위에 start 출력
        self.__button_text.append(
            self.__start_font.render("Start Game", True, colors.white)
        )
        self.__button_rect.append(
            pygame.Rect(
                0, 0, self.user_space.width * 2 / 3, self.user_space.height * 2 / 3
            )
        )
        self.__button_rect[-1].centerx = self.user_space.centerx
        self.__button_rect[-1].centery = self.user_space.centery
        self.__start_surface = pygame.Surface(
            (self.user_space.width * 2 / 3, self.user_space.height * 2 / 3)
        )
        self.__start_surface.fill((196, 216, 214))
        self.__start_text_rect = self.__button_text[-1].get_rect(
            center=self.__start_surface.get_rect().center
        )
        self.__start_surface.blit(self.__button_text[-1], self.__start_text_rect)

        # 봇 이름 리스트 및 이름 공간 사각형 정의
        self.bot_names = [
            "Computer One",
            "Computer Two",
            "Computer Three",
            "Computer Four",
            "Computer Five",
        ]
        self.bot_names_text = [
            self.__game_font.render(self.bot_names[i], True, colors.white)
            for i in range(len(self.bot_names))
        ]
        self.bot_names_rects = [
            self.bot_names_text[i].get_rect(topleft=self.bots_space[i].topleft)
            for i in range(len(self.bot_names))
        ]
        self.bot_name_inputs = [
            (self.bot_names_rects[i], self.bot_names_text[i]) for i in range(5)
        ]

        # 다섯 공간과 봇의 이름을 저장하는 set
        self.bots = [
            (self.bots_space[i], self.bot_names[i]) for i in range(5)
        ]

        # 각 공간에 대한 empty surface
        self.empty_surface = pygame.Surface(self.bots_space_size)
        self.empty_surface.fill(colors.white)

        # empty surface 위에 테두리 그리고 글자 쓰기
        pygame.draw.rect(self.empty_surface, colors.black, self.empty_surface.get_rect(), int(screen_size[1] * (1/100)))
        self.empty_text = self.__game_font.render("empty", True, colors.light_gray)
        self.empty_text_rect = self.empty_text.get_rect(center = self.empty_surface.get_rect().center)
        self.empty_surface.blit(self.empty_text, self.empty_text_rect)

        # 각 봇이 눌린 상태인지 저장하기 위한 딕셔너리
        self.pressed_bots = {
            (self.bots_space[0].x, self.bots_space[0].y): self.__game_settings["pressed_bots"].get("bot1"),
            (self.bots_space[1].x, self.bots_space[1].y): self.__game_settings["pressed_bots"].get("bot2"),
            (self.bots_space[2].x, self.bots_space[2].y): self.__game_settings["pressed_bots"].get("bot3"),
            (self.bots_space[3].x, self.bots_space[3].y): self.__game_settings["pressed_bots"].get("bot4"),
            (self.bots_space[4].x, self.bots_space[4].y): self.__game_settings["pressed_bots"].get("bot5")
            }

        # 봇 영역 버튼 리스트에 추가
        for i in range(len(self.bots_space)):
            self.__button_rect.append(self.bots_space[i])

        # 사용자 이름 수정하고 있는지
        self.user_name_editing = False

    @overrides
    def refresh(self):
        pygame.display.set_caption("Game Lobby")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN
        # 스크린 생성
        self.__screen = pygame.display.set_mode(
            self.__settings.get_screen_resolution(), flag
        )
        self.__button_text = []
        self.__button_rect = []
        self.render()
        return None

    @overrides
    def draw(self):
        # 스크린 채우기
        self.__screen.fill(colors.black)
        self.__screen.blit(self.surface, (0, 0))

        # 각 공간 그리기
        pygame.draw.rect(self.__screen, (50, 100, 80), self.deck_space)
        pygame.draw.rect(self.__screen, (80, 120, 80), self.user_space)
        pygame.draw.rect(self.__screen, colors.white, self.user_space, width=2)

        # 봇 영역 - 회색, 빨간색 테두리, 하얀색 봇 이름
        for i in range(len(self.bots_space)):
            # 눌린 상태인 경우 empty
            if self.pressed_bots.get((self.bots_space[i].x, self.bots_space[i].y)):
                self.__screen.blit(self.empty_surface, self.bots_space[i])
            # 아닌 경우 봇 영역
            else:
                pygame.draw.rect(self.__screen, (50, 50, 50), self.bots_space[i])
                pygame.draw.rect(self.__screen, colors.red, self.bots_space[i], width=2)
                self.__screen.blit(self.bot_names_text[i], self.__button_rect[i+2])

        # 스크린 위에 뒤로가기 버튼, 스타트 버튼 그리기
        self.__screen.blit(self.__button_text[0], self.__button_rect[0])
        self.__screen.blit(self.__start_surface, self.__button_rect[1])

        # 사용자 이름 렌더링
        self.user_name = self.__game_settings.get("user_name", None)
        self.user_name_surface = self.__game_font.render(self.user_name, True, colors.white)
        self.user_name_rect = self.user_name_surface.get_rect()
        self.user_name_rect.center = self.deck_space.center

        # 유저 이름 화면에 출력
        self.__screen.blit(self.user_name_surface, self.user_name_rect)
        if self.user_name_editing:
            pygame.draw.rect(self.__screen, colors.white, self.user_name_rect, 2)

        return None

    @overrides
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_rect)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    self.sounds.play_effect('click')
                    return self.__button_func(i)
            if not self.user_name_editing and self.user_name_rect.collidepoint(mouse_pos):
                self.sounds.play_effect('click')
                self.user_name_editing = True
            elif self.user_name_editing and not self.user_name_rect.collidepoint(mouse_pos):
                self.sounds.play_effect('click')
                self.user_name_editing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return pygame.event.post(
                    pygame.event.Event(events.CHANGE_SCENE, target="main")
                )
            if self.user_name_editing:
                if event.key == pygame.K_BACKSPACE and len(self.user_name) > 1:
                    self.__game_settings.update(user_name = self.user_name[:-1])
                elif event.unicode.isprintable() and len(self.user_name) < 30:
                    self.__game_settings.update(user_name = self.user_name + event.unicode)
                elif event.key == pygame.K_RETURN:
                    self.user_name_editing = False
                self.save_game_settings()
            else:
                if event.key == pygame.K_RETURN:
                    self.user_name_editing = True

        return "continue"

    def __button_func(self, i):
        # 뒤로 가기 버튼
        if i == 0:
            self.__settings.previous_gamelobby()
            return pygame.event.post(
                pygame.event.Event(events.CHANGE_SCENE, target="main")
            )
        # 게임 시작 버튼
        elif i == 1:
            self.__settings.previous_gamelobby()
            return pygame.event.post(
                pygame.event.Event(
                    events.CHANGE_SCENE,
                    target="gameui",
                    args={"game": Game(self.__game_settings.get("player_count, None"))},
                )
            )
        # 봇 추가/삭제 버튼. 없을 때도 버튼이 활성화 되어 있음. 봇 1~5
        elif 1 < i < 7:
            # 이미 눌린 상태인 경우 다시 원래대로 돌리기
            if self.pressed_bots.get((self.bots_space[i-2].x, self.bots_space[i-2].y), None):
                self.pressed_bots[(self.bots_space[i-2].x, self.bots_space[i-2].y)] = not self.pressed_bots.get((self.bots_space[i-2].x, self.bots_space[i-2].y), None)
                self.__game_settings["player_count"] += 1
                self.__game_settings["pressed_bots"][f"bot{i-1}"] = not self.__game_settings["pressed_bots"][f"bot{i-1}"]
                self.save_game_settings()
            # 아닌 경우 empty 추가하기
            else:
                # bot이 2명 이상일 경우
                if self.__game_settings.get("player_count", None) > 2:
                    self.pressed_bots[(self.bots_space[i-2].x, self.bots_space[i-2].y)] = True
                    self.__game_settings["player_count"] -= 1
                    self.__game_settings["pressed_bots"][f"bot{i-1}"] = not self.__game_settings["pressed_bots"][f"bot{i-1}"]
                    self.save_game_settings()
                # bot이 1명일 경우
                else:
                    pass
            print(f"clicked {i}")
            pass

        return None
