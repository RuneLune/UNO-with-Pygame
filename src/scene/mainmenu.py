from .scene import Scene
from overrides import overrides

from gameobj.mainmenu.titletxt import TitleText
from gameobj.mainmenu.playbtn import PlayButton
from gameobj.mainmenu.stagebtn import StageButton
from gameobj.mainmenu.settingsbtn import SettingsButton
from gameobj.mainmenu.quitbtn import QuitButton
from metaclass.singleton import SingletonMeta


class MainMenu(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.title_text = TitleText()
        self.play_button = PlayButton()
        self.stage_button = StageButton()
        self.settings_button = SettingsButton()
        self.quit_button = QuitButton()

        self.play_button.attach(self.scene_manager)
        self.stage_button.attach(self.scene_manager)
        self.settings_button.attach(self.scene_manager)
        self.quit_button.attach(self.scene_manager)

        self.instantiate(self.title_text)
        self.instantiate(self.play_button)
        self.instantiate(self.stage_button)
        self.instantiate(self.settings_button)
        self.instantiate(self.quit_button)

        return None
