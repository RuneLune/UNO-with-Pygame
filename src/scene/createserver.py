from overrides import overrides

from .scene import Scene
from server.server import SocketServer


class CreateServer(Scene):
    @overrides
    def start(self) -> None:
        server = SocketServer()
        server.initialize()
        
        return None
