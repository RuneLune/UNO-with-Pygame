import pygame
from typing import Dict, Type

from settings_function import Settings
import events

# from game_scene import Game_Scene
from main_scene import Main_Scene
from settings_scene import Settings_Scene
from gameUI import Game_UI
from game_lobby import Game_Lobby
from scene import Scene
from stage_select import Stage
from sound import SoundManager
from resource_manager import image_resource


class App:
    MAX_Inst = 1
    Inst_created = 0

    # App 클래스 생성자
    def __new__(cls, *args, **kwargs):
        if cls.Inst_created >= cls.MAX_Inst:
            raise ValueError("Cannot create more App object")
        cls.Inst_created += 1
        return super(App, cls).__new__(cls)

    # App 객체 초기화 메서드
    def __init__(self) -> None:
        pygame.init()

        self.app_icon: pygame.Surface = pygame.image.load(image_resource("icon.png"))

        self.settings: Settings = Settings()
        self.sound_manager: SoundManager = SoundManager(self.settings)

        self.fps: int = 30
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.current_scene: str = "main"

        self.scenes: Dict[str, Type[Scene]] = {
            "main": Main_Scene(self.settings, self.sound_manager),
            "gamelobby": Game_Lobby(self.settings, self.sound_manager),
            "settings": Settings_Scene(self.settings, self.sound_manager),
            "gameui": Game_UI(self.settings, self.sound_manager),
            "stage": Stage(self.settings, self.sound_manager),
        }

        pygame.display.set_icon(self.app_icon)
        pygame.display.set_caption("Main Menu")
        return None

    def start(self) -> None:
        # Main loop
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pass
                elif event.type == events.CHANGE_SCENE:
                    self.current_scene = event.target
                    if hasattr(event, "args"):
                        self.scenes[self.current_scene].get_args(event.args)
                        pass
                    self.scenes[self.current_scene].refresh()
                    continue
                elif event.type == events.CHANGE_SETTINGS:
                    self.sound_manager.refresh()
                    self.scenes[self.current_scene].refresh()
                    pass
                elif event.type == events.GAME_END:
                    self.scenes["stage"].handle(event)
                    self.scenes[self.current_scene].handle(event)
                    pass
                else:
                    self.scenes[self.current_scene].handle(event)
                    pass

            self.scenes[self.current_scene].draw()

            # Update screen
            pygame.display.flip()
            self.clock.tick(self.fps)
            continue

        # Quit pygame
        pygame.quit()
        return None
