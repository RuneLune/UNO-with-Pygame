from .scene import Scene
from overrides import overrides

from gameobj.scene1.bg import Background
from gameobj.scene1.startbtn import StartButton
from metaclass.singleton import SingletonMeta


class Scene1(Scene, metaclass=SingletonMeta):
    @overrides
    def start(self) -> None:
        self.background = Background()
        self.start_button = StartButton()

        self.start_button.on_mouse_up_as_button = lambda: self.scene_manager.load_scene(
            "scene2"
        )

        # 장면 전환 기능이 있는 버튼 오브젝트(StartButton)에 옵저버(SceneManager) 추가
        # self.start_button.attach(self.scene_manager)

        # 장면에 게임 오브젝트 추가
        self.instantiate(self.background)
        self.instantiate(self.start_button)

        return None
