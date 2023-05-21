from overrides import overrides

from .scene import Scene
from server.server import SocketServer


class CreateServer(Scene):
    @overrides
    def update(self) -> None:
        if not hasattr(self, "update_called"):
            self.update_called = True
            server = SocketServer()
            if (
                self.scene_manager.back_scene_name is not None
                and self.scene_manager.back_scene_name == "multi_lobby"
            ):
                server.close()
                self.scene_manager.load_scene("main_menu")
                pass
            elif self.scene_manager.previous_scene_name == "main_menu":
                server.initialize()
                self.scene_manager.load_scene("multi_lobby")
                pass
            else:
                pass
            pass
        return None
