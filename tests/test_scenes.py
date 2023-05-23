import os
import sys
import pygame

# import time

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from manager.scenemgr import SceneManager
from scene.achieve_scene import AchieveScene
from scene.cfgmenu import ConfigMenu
from scene.createserver import CreateServer
from scene.game_scene import GameScene
from scene.gamelobby import GameLobby
from scene.joinserver import JoinServer
from scene.mainmenu import MainMenu
# from scene.multilobby import MultiLobby
from scene.quit import QuitScene
from scene.story_scene import StoryScene

pygame.init()
pygame.display.set_mode((800, 600))

scene_manager = SceneManager()


def test_AchieveScene() -> None:
    try:
        achieve_scene: AchieveScene = AchieveScene(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_ConfigMenu() -> None:
    try:
        achieve_scene: ConfigMenu = ConfigMenu(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_CreateServer() -> None:
    try:
        achieve_scene: CreateServer = CreateServer(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_GameScene() -> None:
    try:
        achieve_scene: GameScene = GameScene(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_GameLobby() -> None:
    try:
        achieve_scene: GameLobby = GameLobby(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_JoinServer() -> None:
    try:
        achieve_scene: JoinServer = JoinServer(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_MainMenu() -> None:
    try:
        achieve_scene: MainMenu = MainMenu(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


# def test_MultiLobby() -> None:
#     try:
#         achieve_scene: MultiLobby = MultiLobby(scene_manager)
#         achieve_scene.update()
#         achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
#         achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
#         achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
#         achieve_scene.exit()
#         pass
#     except Exception:
#         assert False
#         pass
#     assert True
#     return None


def test_QuitScene() -> None:
    try:
        achieve_scene: QuitScene = QuitScene(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_StoryScene() -> None:
    try:
        achieve_scene: StoryScene = StoryScene(scene_manager)
        achieve_scene.update()
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEBUTTONUP))
        achieve_scene.handle(pygame.event.Event(pygame.MOUSEMOTION))
        achieve_scene.exit()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None
