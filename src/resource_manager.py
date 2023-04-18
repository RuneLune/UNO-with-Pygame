import sys
import os


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "res", relative_path)


def font_resource(font_file_path: str) -> str:
    return resource_path(os.path.join("font", font_file_path))


def image_resource(image_file_path: str) -> str:
    return resource_path(os.path.join("img", image_file_path))


def sound_resource(sound_file_path: str) -> str:
    return resource_path(os.path.join("sound", sound_file_path))
