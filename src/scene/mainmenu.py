from overrides import overrides

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.mainmenu.titletxt import TitleText
from gameobj.mainmenu.menu import Menu
from gameobj.mainmenu.keybind import KeyBind
from gameobj.mainmenu.keyinput import KeyInput
from gameobj.mainmenu.selector import Selector


class MainMenu(Scene):
    @overrides
    def start(self) -> None:
        self.instantiate(BackgroundObject(color.white))
        self.instantiate(TitleText("UNO"))

        Menu.destroy_all()
        play_menu = Menu("Play").attach_mgr(self.scene_manager, "gamelobby")
        multiplayer_menu = Menu("Multiplayer").attach_mgr(
            self.scene_manager, "multilobby"
        )
        stage_menu = Menu("Stage").attach_mgr(self.scene_manager, "story_scene")
        achievements_menu = Menu("Achievements").attach_mgr(self.scene_manager, "test")
        config_menu = Menu("Settings").attach_mgr(self.scene_manager, "config_menu")
        quit_menu = Menu("Quit").attach_mgr(self.scene_manager, "quit")
        self.instantiate(play_menu)
        self.instantiate(multiplayer_menu)
        self.instantiate(stage_menu)
        self.instantiate(achievements_menu)
        self.instantiate(config_menu)
        self.instantiate(quit_menu)

        KeyBind.destroy_all()
        self.instantiate(KeyBind("Left"))
        self.instantiate(KeyBind("Right"))
        self.instantiate(KeyBind("Up"))
        self.instantiate(KeyBind("Down"))
        self.instantiate(KeyBind("Select"))
        self.instantiate(KeyBind("Cancel"))

        selector = Selector()
        self.instantiate(selector)

        key_input = KeyInput().attach_selector(selector)
        self.instantiate(key_input)

        key_input.attach_menu(
            [
                play_menu,
                multiplayer_menu,
                stage_menu,
                achievements_menu,
                config_menu,
                quit_menu,
            ]
        )

        return None
