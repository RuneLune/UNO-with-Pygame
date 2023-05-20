from overrides import overrides

from .scene import Scene
from server.server import SocketServer


class CreateServer(Scene):
    @overrides
    def update(self) -> None:
        if not hasattr(self, "update_called"):
            self.update_called = True
            server = SocketServer()
            server.initialize()
            self.scene_manager.load_scene("multilobby")
        return None
