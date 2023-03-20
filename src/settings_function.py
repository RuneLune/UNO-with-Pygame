import pygame
import copy
import json
import os
import ctypes  # Get Resolution of PC


initial_settings = {
    "screen_size": (1280, 720),
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
        
        # Return 0 if save was successful
        return 0

    def get_settings(self):
        return copy.deepcopy(self.__settings)

    # 800*600 Screen
    def SVGA(self):
        self.__settings.update(screen_size=(800, 600))

    # 1280*720 Screen
    def HD(self):
        self.__settings.update(screen_size=(1280, 720))

    # 1920*1080 Screen
    def FHD(self):
        self.__settings.update(screen_size=(1920, 1080))

    # Fullscreen
    def fullScreen(self):
        user32 = ctypes.windll.user32
        self.__settings.update(
            screen_size=(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        )  # Get resolution
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.FULLSCREEN
        )  # Fullscreen setting
