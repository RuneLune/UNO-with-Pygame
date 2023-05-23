from overrides import overrides

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.mainmenu.titletxt import TitleText
from gameobj.mainmenu.menu import Menu
from gameobj.mainmenu.keybind import KeyBind
from gameobj.mainmenu.keyinput import KeyInput
from gameobj.mainmenu.selector import Selector
from gameobj.mainmenu.bg import Back
from gameobj.mainmenu.backbtn import BackButton

from manager.soundmgr import SoundManager


class SelectMenu(Scene):
    @overrides
    def start(self) -> None:
        self.instantiate(BackgroundObject(color.white))

        back = Back()

        Menu.destroy_all()
        # play_menu = Menu("Play").attach_mgr(self.scene_manager, "gamelobby")
        server_menu = Menu("Create Room").attach_mgr(
            self.scene_manager, "create_server"
        )
        client_menu = Menu("Join Room").attach_mgr(self.scene_manager, "join_server")
        # stage_menu = Menu("Story").attach_mgr(self.scene_manager, "story_scene")
        # achievements_menu = Menu("Achievements").attach_mgr(
        #     self.scene_manager, "achievements"
        # )
        # config_menu = Menu("Settings").attach_mgr(self.scene_manager, "config_menu")
        # quit_menu = Menu("Quit").attach_mgr(self.scene_manager, "quit")
        # self.instantiate(play_menu)
        self.instantiate(server_menu)
        self.instantiate(client_menu)
        backbutton = BackButton("Back").attach_mgr(self.scene_manager)
        # backbutton.color = color.black
        self.instantiate(backbutton)
        # self.instantiate(stage_menu)
        # self.instantiate(achievements_menu)
        # self.instantiate(config_menu)
        # self.instantiate(quit_menu)
        # self.instantiate(back)

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
                # play_menu,
                server_menu,
                client_menu,
                # stage_menu,
                # achievements_menu,
                # config_menu,
                # quit_menu,
            ]
        )

        SoundManager().play_main_background_sound()

        return None
