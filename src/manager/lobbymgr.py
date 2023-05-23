import copy
import json
import os
import pygame
from typing import Dict

from util.appdata_manager import game_config_path
from metaclass.singleton import SingletonMeta

initial_settings: Dict[str, int | Dict[str, bool] | str | str] = {
    "player_count": 2,
    "active_bots": {
        "bot1": True,
        "bot2": False,
        "bot3": False,
        "bot4": False,
        "bot5": False,
    },
    "user_name": " User_Name ",
    "bot_type": "Normal",
}


class LobbyManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        global initial_settings
        self.__game_settings = initial_settings
        # Create settings.json if not exist
        if not os.path.isfile(game_config_path):
            self.reset_game_settings()
            self.save_game_settings()
        else:
            self.load_game_settings()

        return super().__init__()

    # Settings load method
    def load_game_settings(self):
        # load saved settings from file
        if os.path.isfile(game_config_path):
            try:
                with open(game_config_path, "r") as f:
                    self.__game_settings = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass

    # Settings reset method
    def reset_game_settings(self):
        global initial_settings
        self.__game_settings = copy.deepcopy(initial_settings)
        self.save_game_settings()

    # Settings save method
    def save_game_settings(self):
        try:
            # Save settings to file
            with open(game_config_path, "w") as f:
                json.dump(self.__game_settings, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load_game_settings()
        # Return 0 if save was successful
        return 0

    def get_game_settings(self):
        return copy.deepcopy(self.__game_settings)

    def bot1_toggle(self):
        self.__game_settings["active_bots"]["bot1"] = not self.__game_settings[
            "active_bots"
        ]["bot1"]
        self.save_game_settings()

    def bot2_toggle(self):
        self.__game_settings["active_bots"]["bot2"] = not self.__game_settings[
            "active_bots"
        ]["bot2"]
        self.save_game_settings()

    def bot3_toggle(self):
        self.__game_settings["active_bots"]["bot3"] = not self.__game_settings[
            "active_bots"
        ]["bot3"]
        self.save_game_settings()

    def bot4_toggle(self):
        self.__game_settings["active_bots"]["bot4"] = not self.__game_settings[
            "active_bots"
        ]["bot4"]
        self.save_game_settings()

    def bot5_toggle(self):
        self.__game_settings["active_bots"]["bot5"] = not self.__game_settings[
            "active_bots"
        ]["bot5"]
        self.save_game_settings()

    def set_player_count(self, value: int):
        self.__game_settings["player_count"] = value
        self.save_game_settings()

    def user_name_change(self):
        while True:
            event = pygame.event
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_BACKSPACE
                    and len(self.__game_settings["user_name"]) > 1
                ):
                    self.__game_settings.update(
                        {"user_name": self.__game_settings["user_name"][:-1]}
                    )
                elif (
                    event.unicode.isprintable()
                    and len(self.__game_settings["user_name"]) < 20
                ):
                    self.__game_settings.update(
                        {"user_name": self.__game_settings["user_name"] + event.unicode}
                    )
                elif event.key == pygame.K_RETURN:
                    break
                else:
                    pass
                self.save_game_settings()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                break
            else:
                pass
        return None

    @property
    def user_name(self):
        return self.__game_settings["user_name"]

    @user_name.setter
    def user_name(self, value: str):
        self.__game_settings["user_name"] = value
        self.save_game_settings()

    def set_bot_type(self, value: str):
        self.__game_settings["bot_type"] = value
        self.save_game_settings()
