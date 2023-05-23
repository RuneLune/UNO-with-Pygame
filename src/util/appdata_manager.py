import sys
import os
from appdata import AppDataPaths


def appdata_path(relative_path: str) -> str:
    # if hasattr(sys, "_MEIPASS"):
    #     base_path = AppDataPaths("SE2023_09")
    #     pass
    # else:
    #     base_path = os.path.join(os.path.abspath("."), ".appdata")
    #     pass
    base_path = os.path.join(os.path.abspath("."), ".appdata")

    if not os.path.exists(base_path):
        os.mkdir(base_path)
        pass

    return os.path.join(base_path, relative_path)


def config_data_path(file_name: str) -> str:
    base_path = appdata_path("config")
    if not os.path.exists(base_path):
        os.mkdir(base_path)
        pass

    return os.path.join(base_path, file_name)


def game_data_path(file_name: str) -> str:
    base_path = appdata_path("game")
    if not os.path.exists(base_path):
        os.mkdir(base_path)
        pass

    return os.path.join(base_path, file_name)


config_path: str = appdata_path("config.json")
stage_access_path: str = game_data_path("access.json")
game_config_path: str = game_data_path("config.json")
achieve_path: str = game_data_path("achieve.json")
