import os
import sys
import pygame
import time

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from game import Game
from stage_a import Stage_A
from stage_b import Stage_B
from stage_c import Stage_C
from stage_d import Stage_D

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
        stage_a: Stage_A = Stage_A()
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
        stage_b: Stage_B = Stage_B()
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
        stage_c: Stage_C = Stage_C()
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
        stage_d: Stage_D = Stage_D()
        time.sleep(5)
        stage_d.tick()
        pass
    except Exception:
        assert False
        pass
    assert True
    return None
