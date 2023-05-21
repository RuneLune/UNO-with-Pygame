from overrides import overrides

from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.joinserver.keyinput import KeyInput
from gameobj.joinserver.iptxt import IPText
import util.colors as color


class JoinServer(Scene):
    @overrides
    def start(self) -> None:
        self.instantiate(BackgroundObject(color.white))
        self.key_input = KeyInput().attach_mgr(self.scene_manager)
        self.instantiate(self.key_input)
        self.instantiate(IPText())
        return None

    pass
