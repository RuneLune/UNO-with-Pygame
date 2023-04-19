import pygame
import copy
import json
import os
from screeninfo import get_monitors
from typing import Tuple, Dict

from util.appdata_manager import config_path


initial_settings: Dict[str, str | bool | Dict[str, int] | float] = {
    "screen_size": "SVGA",
    "full_screen": False,
    "key_settings": {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "select": pygame.K_RETURN,
        "cancel": pygame.K_ESCAPE,
    },
    "colorblind_mode": False,
    "previous_scene": "main",
    "background_sound_volume": 1,
    "effect_sound_volume": 0.5,
    "all_sound_volume": 1,
}


class Settings:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self) -> None:
        global initial_settings
        self.__settings = initial_settings
        # Create settings.json if not exist
        if not os.path.isfile(config_path):
            self.reset_settings()
            self.save_settings()
        else:
            self.load_settings()

        return super().__init__()

    # Settings load method
    def load_settings(self):
        # load saved settings from file
        if os.path.isfile(config_path):
            try:
                with open(config_path, "r") as f:
                    self.__settings = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass
        self.set_screen_resolution()

    # Settings reset method
    def reset_settings(self):
        global initial_settings
        copy_previous = self.__settings.get("previous_scene", None)
        self.__settings = copy.deepcopy(initial_settings)
        self.__settings.update(previous_scene=copy_previous)

    # Settings save method
    def save_settings(self):
        try:
            # Save settings to file
            with open(config_path, "w") as f:
                json.dump(self.__settings, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load_settings()
        # Return 0 if save was successful
        return 0

    def get_settings(self):
        return copy.deepcopy(self.__settings)

    def set_screen_resolution(self):
        if self.__settings.get("fullscreen", False) is False:
            screen_type = self.__settings.get("screen_size", "SVGA")
            if screen_type == "SVGA":
                self.__SVGA()
            elif screen_type == "HD":
                self.__HD()
            elif screen_type == "FHD":
                self.__FHD()
            else:
                self.__settings.update(screen_size="SVGA")
                self.__SVGA()
        else:
            self.__fullscreen()

    def get_screen_resolution(self) -> Tuple[int, int]:
        return self.__screen_resolution

    def lower_screen_size(self):
        if self.__settings.get("screen_size", None) == "SVGA":
            self.__settings.update(screen_size="FHD")
            self.__FHD()
        elif self.__settings.get("screen_size", None) == "HD":
            self.__settings.update(screen_size="SVGA")
            self.__SVGA()
        elif self.__settings.get("screen_size", None) == "FHD":
            self.__settings.update(screen_size="HD")
            self.__HD()
        self.save_settings()

    def higher_screen_size(self):
        if self.__settings.get("screen_size", None) == "SVGA":
            self.__settings.update(screen_size="HD")
            self.__HD()
        elif self.__settings.get("screen_size", None) == "HD":
            self.__settings.update(screen_size="FHD")
            self.__FHD()
        elif self.__settings.get("screen_size", None) == "FHD":
            self.__settings.update(screen_size="SVGA")
            self.__SVGA()
        self.save_settings()

    def higher_background_sound_volume(self):
        if self.__settings.get("background_sound_volume", None) == 0:
            self.__settings.update(background_sound_volume=0.5)
        elif self.__settings.get("background_sound_volume", None) == 0.5:
            self.__settings.update(background_sound_volume=1)
        elif self.__settings.get("background_sound_volume", None) == 1:
            self.__settings.update(background_sound_volume=0)
        self.save_settings()

    def lower_background_sound_volume(self):
        if self.__settings.get("background_sound_volume", None) == 0:
            self.__settings.update(background_sound_volume=1)
        elif self.__settings.get("background_sound_volume", None) == 0.5:
            self.__settings.update(background_sound_volume=0)
        elif self.__settings.get("background_sound_volume", None) == 1:
            self.__settings.update(background_sound_volume=0.5)
        self.save_settings()

    def higher_effect_sound_volume(self):
        if self.__settings.get("effect_sound_volume", None) == 0:
            self.__settings.update(effect_sound_volume=0.5)
        elif self.__settings.get("effect_sound_volume", None) == 0.5:
            self.__settings.update(effect_sound_volume=1)
        elif self.__settings.get("effect_sound_volume", None) == 1:
            self.__settings.update(effect_sound_volume=0)
        self.save_settings()

    def lower_effect_sound_volume(self):
        if self.__settings.get("effect_sound_volume", None) == 0:
            self.__settings.update(effect_sound_volume=1)
        elif self.__settings.get("effect_sound_volume", None) == 0.5:
            self.__settings.update(effect_sound_volume=0)
        elif self.__settings.get("effect_sound_volume", None) == 1:
            self.__settings.update(effect_sound_volume=0.5)
        self.save_settings()

    def higher_all_sound_volume(self):
        if self.__settings.get("all_sound_volume", None) == 0:
            self.__settings.update(all_sound_volume=0.5)
        elif self.__settings.get("all_sound_volume", None) == 0.5:
            self.__settings.update(all_sound_volume=1)
        elif self.__settings.get("all_sound_volume", None) == 1:
            self.__settings.update(all_sound_volume=0)
        self.save_settings()

    def lower_all_sound_volume(self):
        if self.__settings.get("all_sound_volume", None) == 0:
            self.__settings.update(all_sound_volume=1)
        elif self.__settings.get("all_sound_volume", None) == 0.5:
            self.__settings.update(all_sound_volume=0)
        elif self.__settings.get("all_sound_volume", None) == 1:
            self.__settings.update(all_sound_volume=0.5)
        self.save_settings()

    def previous_main(self):
        self.__settings.update(previous_scene="main")
        self.save_settings()

    def previous_gamelobby(self):
        self.__settings.update(previous_scene="gamelobby")
        self.save_settings()

    def previous_gameui(self):
        self.__settings.update(previous_scene="gameui")
        self.save_settings()

    def previous_none(self):
        self.__settings.update(previous_scene=None)
        self.save_settings()

    def previous_stageselect(self):
        self.__settings.update(previous_scene="stageselect")
        self.save_settings()

    def change_fullscreen(self):
        if self.__settings.get("fullscreen", False) is False:
            self.__settings.update(fullscreen=True)
        else:
            self.__settings.update(fullscreen=False)
        self.set_screen_resolution()
        self.save_settings()

    def change_colorblind_mode(self):
        if self.__settings.get("colorblind_mode", False) is False:
            self.__settings.update(colorblind_mode=True)
        else:
            self.__settings.update(colorblind_mode=False)
        self.save_settings()

    # 800*600 Screen
    def __SVGA(self):
        self.__screen_resolution = (800, 600)

    # 1280*720 Screen
    def __HD(self):
        self.__screen_resolution = (1280, 720)

    # 1920*1080 Screen
    def __FHD(self):
        self.__screen_resolution = (1920, 1080)

    # Fullscreen
    def __fullscreen(self):
        monitor = get_monitors()[0]
        self.__screen_resolution = (
            monitor.width,
            monitor.height,
        )

    def set_key_value(self, key_name, value):
        self.__settings["key_settings"][key_name] = value
        self.save_settings()

    def key_change(self):
        temp = 0
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                temp = event.key
                if (
                    temp == self.__settings["key_settings"]["left"]
                    or temp == self.__settings["key_settings"]["right"]
                    or temp == self.__settings["key_settings"]["up"]
                    or temp == self.__settings["key_settings"]["down"]
                    or temp == self.__settings["key_settings"]["select"]
                    or temp == self.__settings["key_settings"]["cancel"]
                ):
                    pass
                else:
                    break
        return temp
