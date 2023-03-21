import pygame
import copy
import json
import os
import ctypes  # Get Resolution of PC


initial_settings = {
    "screen_size": "SVGA",
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
        self.__screen_resolution = self.get_screen_size(
            self.__settings.get("screen_size", None)
        )

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

    def get_screen_size(self, screen_type):
        if screen_type == "SVGA":
            return (800, 600)
        elif screen_type == "HD":
            return (1280, 720)
        elif screen_type == "FHD":
            return (1920, 1080)
        elif screen_type == "Full Screen":
            return (
                ctypes.windll.user32.GetSystemMetrics(0),
                ctypes.windll.user32.GetSystemMetrics(1),
            )
        else:
            self.__settings.update(screen_size="SVGA")
            return (800, 600)

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
    def __fullScreen(self):
        user32 = ctypes.windll.user32
        self.__settings.update(
            screen_size=(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        )  # Get resolution
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.FULLSCREEN
        )  # Fullscreen setting
