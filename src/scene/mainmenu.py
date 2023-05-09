from overrides import overrides
import pygame

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.mainmenu.titletxt import TitleText
from gameobj.mainmenu.menu import Menu


class MainMenu(Scene):
    @overrides
    def start(self) -> None:
        self.play_button = Menu("Play").attach_mgr(self.scene_manager)
        self.stage_button = Menu("Stage").attach_mgr(self.scene_manager)
        self.achievements_button = Menu("Achievements").attach_mgr(self.scene_manager)
        self.settings_button = Menu("Settings").attach_mgr(self.scene_manager)
        self.quit_button = Menu("Quit").attach_mgr(self.scene_manager)

        self.play_button.target_scene = "gamelobby"
        self.stage_button.target_scene = "story_scene"
        self.achievements_button.target_scene = "achievements_scene"
        self.settings_button.target_scene = "config_menu"
        self.quit_button.target_scene = "quit_scene"

        self.quit_button.on_mouse_up_as_button = lambda: pygame.event.post(
            pygame.event.Event(pygame.QUIT)
        )

        self.instantiate(BackgroundObject(color.white))
        self.instantiate(TitleText("UNO"))
        self.instantiate(self.play_button)
        self.instantiate(self.stage_button)
        self.instantiate(self.achievements_button)
        self.instantiate(self.settings_button)
        self.instantiate(self.quit_button)

        return None
