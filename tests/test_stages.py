import os
import sys
import pygame
import time

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from game.game import Game
from game.stage_a import StageA
from game.stage_b import StageB
from game.stage_c import StageC
from game.stage_d import StageD

pygame.init()


def test_game() -> None:
    try:
        game: Game = Game(6)
        time.sleep(5)
        game.tick()
        game.pause_timer()
        game.resume_timer()
        game.end_turn()
        game._shuffle()
        time.sleep(5)
        game.tick()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_stage_a() -> None:
    try:
        stage_a: StageA = StageA()
        time.sleep(5)
        stage_a.tick()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_stage_b() -> None:
    try:
        stage_b: StageB = StageB()
        time.sleep(5)
        stage_b.tick()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_stage_c() -> None:
    try:
        stage_c: StageC = StageC()
        time.sleep(5)
        stage_c.tick()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None


def test_stage_d() -> None:
    try:
        stage_d: StageD = StageD()
        time.sleep(5)
        stage_d.tick()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None
