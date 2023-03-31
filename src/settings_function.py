import pygame
import copy
import json
import os
import ctypes  # Get Resolution of PC


initial_settings = {
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
}


class Settings:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        # Create settings.json if not exist
        if not os.path.isfile("settings.json"):
            self.reset_settings()
            self.save_settings()
        else:
            self.load_settings()

        return super().__init__()

    # Settings load method
    def load_settings(self):
        # load saved settings from file
        if os.path.isfile("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    self.__settings = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass
        self.set_screen_resolution()

    # Settings reset method
    def reset_settings(self):
        global initial_settings
        self.__settings = copy.deepcopy(initial_settings)

    # Settings save method
    def save_settings(self):
        try:
            # Save settings to file
            with open("settings.json", "w") as f:
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

    def get_screen_resolution(self):
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
        self.__screen_resolution = (
            ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1),
        )
