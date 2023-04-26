from .scene import Scene
from overrides import overrides

from gameobj.scene1.startbtn import StartButton
from metaclass.singleton import SingletonMeta


class Scene1(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        start_button = StartButton()
        start_button.attach(self.scene_manager)
        self.instantiate(start_button)
        return None
