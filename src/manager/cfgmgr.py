import pygame
import copy
import json
import os
from screeninfo import get_monitors
from typing import Tuple, Dict

from util.appdata_manager import config_path
from metaclass.singleton import SingletonMeta


initial_config: Dict[str, str | bool | Dict[str, int] | float] = {
    "screen_size": "SVGA",
    "fullscreen": False,
    "keybindings": {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "select": pygame.K_RETURN,
        "cancel": pygame.K_ESCAPE,
    },
    "volume": {
        "all": 100,
        "bgm": 50,
        "sfx": 50,
    },
    "colorblind_mode": False,
}


class Config(metaclass=SingletonMeta):
    def __init__(self) -> None:
        global initial_config
        self.__config = initial_config
        # Create config.json if not exist
        if not os.path.isfile(config_path):
            self.reset()
            self.save()
        else:
            self.load()

        return super().__init__()

    def get_volume(self, target_volume: str):
        return self.config.get("volume").get(target_volume, 50)

    def set_volume(self, target_volume: str, value: int) -> None:
        self.__config.get("volume").update({target_volume: value})
        self.save()
        return None

    # Config load method
    def load(self):
        # load saved config from file
        if os.path.isfile(config_path):
            try:
                with open(config_path, "r") as f:
                    self.__config = json.load(f)
            except BaseException:
                # Error occurred while loading config from file
                pass
        self.set_screen_resolution()

    # Config reset method
    def reset(self):
        global initial_config
        self.__config = copy.deepcopy(initial_config)
        self.save()

    # Config save method
    def save(self):
        try:
            # Save config to file
            with open(config_path, "w") as f:
                json.dump(self.__config, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load()
        # Return 0 if save was successful
        return 0

    @property
    def config(self):
        return copy.deepcopy(self.__config)

    def set_screen_resolution(self) -> None:
        if self.__config.get("fullscreen", False) is False:
            screen_type = self.__config.get("screen_size", "SVGA")
            if screen_type == "SVGA":
                self.__SVGA()
                pass
            elif screen_type == "HD":
                self.__HD()
                pass
            elif screen_type == "FHD":
                self.__FHD()
                pass
            else:
                self.__config.update(screen_size="SVGA")
                self.__SVGA()
                pass
            pygame.display.set_mode(self.__screen_resolution)
            pass
        else:
            self.__fullscreen()
            pygame.display.set_mode(self.__screen_resolution, pygame.FULLSCREEN)
            pass

        return None

    def get_screen_resolution(self) -> Tuple[int, int]:
        return self.__screen_resolution

    def decrease_screen_size(self):
        if self.__config.get("screen_size", None) == "SVGA":
            self.__config.update(screen_size="FHD")
            self.__FHD()
        elif self.__config.get("screen_size", None) == "HD":
            self.__config.update(screen_size="SVGA")
            self.__SVGA()
        elif self.__config.get("screen_size", None) == "FHD":
            self.__config.update(screen_size="HD")
            self.__HD()
        self.save()

    def increase_screen_size(self):
        if self.__config.get("screen_size", None) == "SVGA":
            self.__config.update(screen_size="HD")
            self.__HD()
        elif self.__config.get("screen_size", None) == "HD":
            self.__config.update(screen_size="FHD")
            self.__FHD()
        elif self.__config.get("screen_size", None) == "FHD":
            self.__config.update(screen_size="SVGA")
            self.__SVGA()
        self.save()

    def higher_background_sound_volume(self):
        if self.__config.get("background_sound_volume", None) == 0:
            self.__config.update(background_sound_volume=0.5)
        elif self.__config.get("background_sound_volume", None) == 0.5:
            self.__config.update(background_sound_volume=1)
        elif self.__config.get("background_sound_volume", None) == 1:
            self.__config.update(background_sound_volume=0)
        self.save()

    def lower_background_sound_volume(self):
        if self.__config.get("background_sound_volume", None) == 0:
            self.__config.update(background_sound_volume=1)
        elif self.__config.get("background_sound_volume", None) == 0.5:
            self.__config.update(background_sound_volume=0)
        elif self.__config.get("background_sound_volume", None) == 1:
            self.__config.update(background_sound_volume=0.5)
        self.save()

    def higher_effect_sound_volume(self):
        if self.__config.get("effect_sound_volume", None) == 0:
            self.__config.update(effect_sound_volume=0.5)
        elif self.__config.get("effect_sound_volume", None) == 0.5:
            self.__config.update(effect_sound_volume=1)
        elif self.__config.get("effect_sound_volume", None) == 1:
            self.__config.update(effect_sound_volume=0)
        self.save()

    def lower_effect_sound_volume(self):
        if self.__config.get("effect_sound_volume", None) == 0:
            self.__config.update(effect_sound_volume=1)
        elif self.__config.get("effect_sound_volume", None) == 0.5:
            self.__config.update(effect_sound_volume=0)
        elif self.__config.get("effect_sound_volume", None) == 1:
            self.__config.update(effect_sound_volume=0.5)
        self.save()

    def higher_all_sound_volume(self):
        if self.__config.get("all_sound_volume", None) == 0:
            self.__config.update(all_sound_volume=0.5)
        elif self.__config.get("all_sound_volume", None) == 0.5:
            self.__config.update(all_sound_volume=1)
        elif self.__config.get("all_sound_volume", None) == 1:
            self.__config.update(all_sound_volume=0)
        self.save()

    def lower_all_sound_volume(self):
        if self.__config.get("all_sound_volume", None) == 0:
            self.__config.update(all_sound_volume=1)
        elif self.__config.get("all_sound_volume", None) == 0.5:
            self.__config.update(all_sound_volume=0)
        elif self.__config.get("all_sound_volume", None) == 1:
            self.__config.update(all_sound_volume=0.5)
        self.save()

    def toggle_fullscreen(self):
        if self.__config.get("fullscreen", False) is False:
            self.__config.update(fullscreen=True)
        else:
            self.__config.update(fullscreen=False)
        self.set_screen_resolution()
        self.save()

    def toggle_colorblind_mode(self):
        if self.__config.get("colorblind_mode", False) is False:
            self.__config.update(colorblind_mode=True)
        else:
            self.__config.update(colorblind_mode=False)
        self.save()
        return None

    def decrease(self, target) -> None:
        if target == "screen_size":
            self.decrease_screen_size()
            pass
        elif target == "fullscreen":
            self.toggle_fullscreen()
            pass
        elif target == "colorblind_mode":
            self.toggle_colorblind_mode()
            pass
        return None

    def increase(self, target) -> None:
        if target == "screen_size":
            self.increase_screen_size()
            pass
        elif target == "fullscreen":
            self.toggle_fullscreen()
            pass
        elif target == "colorblind_mode":
            self.toggle_colorblind_mode()
            pass
        return None

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

    def set_key_value(self, key_name, value) -> bool:
        if value in self.__config["keybindings"].values():
            return False
        self.__config["keybindings"][key_name] = value
        self.save()
        return True

    def key_change(self):
        temp = 0
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                temp = event.key
                if (
                    temp == self.__config["keybindings"]["left"]
                    or temp == self.__config["keybindings"]["right"]
                    or temp == self.__config["keybindings"]["up"]
                    or temp == self.__config["keybindings"]["down"]
                    or temp == self.__config["keybindings"]["select"]
                    or temp == self.__config["keybindings"]["cancel"]
                ):
                    pass
                else:
                    break
        return temp
