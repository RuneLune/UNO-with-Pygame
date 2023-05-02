import pygame

from manager.cfgmgr import Config
from manager.scenemgr import SceneManager
from metaclass.singleton import SingletonMeta


class App(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60
        settings = Config().config
        if settings.get("full_screen", False):
            self.screen = pygame.display.set_mode(
                Config().get_screen_resolution(), pygame.FULLSCREEN
            )
            pass
        else:
            self.screen = pygame.display.set_mode(Config().get_screen_resolution())
        self.scene_manager = SceneManager()

        self.running: bool = True
        return None

    def start(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                else:
                    self.scene_manager.handle_scene(event)
                    pass
                continue
            self.scene_manager.update_scene()

            pygame.display.flip()
            self.clock.tick(self.fps)
            continue

        pygame.quit()
        return None

    pass
