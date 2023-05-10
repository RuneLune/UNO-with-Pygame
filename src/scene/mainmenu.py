from overrides import overrides

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.mainmenu.titletxt import TitleText
from gameobj.mainmenu.menu import Menu
from gameobj.mainmenu.keybind import KeyBind


class MainMenu(Scene):
    @overrides
    def start(self) -> None:
        self.instantiate(BackgroundObject(color.white))
        self.instantiate(TitleText("UNO"))

        Menu.destroy_all()
        self.instantiate(Menu("Play").attach_mgr(self.scene_manager, "gamelobby"))
        self.instantiate(Menu("Stage").attach_mgr(self.scene_manager, "story_scene"))
        self.instantiate(Menu("Achievements").attach_mgr(self.scene_manager, "test"))
        self.instantiate(Menu("Settings").attach_mgr(self.scene_manager, "config_menu"))
        self.instantiate(Menu("Quit").attach_mgr(self.scene_manager, "quit"))

        KeyBind.destroy_all()
        self.instantiate(KeyBind("Left"))
        self.instantiate(KeyBind("Right"))
        self.instantiate(KeyBind("Up"))
        self.instantiate(KeyBind("Down"))
        self.instantiate(KeyBind("Select"))
        self.instantiate(KeyBind("Cancel"))

        return None
