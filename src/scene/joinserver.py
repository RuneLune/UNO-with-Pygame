from overrides import overrides

from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.joinserver.keyinput import KeyInput
from gameobj.joinserver.iptxt import IPText
from client.client import SocketClient
import util.colors as color


class JoinServer(Scene):
    @overrides
    def start(self) -> None:
        self.update_called = False
        self.instantiate(BackgroundObject(color.white))
        self.key_input = KeyInput().attach_mgr(self.scene_manager)
        self.instantiate(self.key_input)
        self.instantiate(IPText())
        return None

    @overrides
    def update(self) -> None:
        if not self.update_called:
            if self.scene_manager.back_scene_name == "multi_lobby":
                self.update_called = True
                SocketClient().close()
                self.scene_manager.load_previous_scene()
                pass
            pass
        return None

    pass
