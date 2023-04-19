import os
import sys
import time

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from util.timer import Timer


def test_timer_normal() -> None:
    timer = Timer()

    try:
        if timer.status() != "stopped":
            assert False
            pass
        timer.start()
        if timer.status() != "running":
            assert False
            pass
        time.sleep(1)
        timer.pause()
        if timer.status() != "paused":
            assert False
            pass
        if abs(timer.get().total_seconds() - 1) > 0.01:
            assert False
            pass
        timer.resume()
        if timer.status() != "running":
            assert False
            pass
        time.sleep(2)
        if abs(timer.get().total_seconds() - 3) > 0.01:
            assert False
            pass
        timer.stop()
        if timer.status() != "stopped":
            assert False
            pass
        pass
    except Exception:
        assert False
        pass
    return None


def test_timer_exceptions() -> None:
    timer = Timer()
    try:
        timer.get()
        assert False
        pass
    except Exception:
        pass
    try:
        timer.pause()
        assert False
        pass
    except Exception:
        pass
    try:
        timer.resume()
        assert False
        pass
    except Exception:
        pass
    try:
        timer.start()
        timer.pause()
        pass
    except Exception:
        assert False
        pass
    try:
        timer.pause()
        assert False
        pass
    except Exception:
        pass
    try:
        timer.resume()
        pass
    except Exception:
        assert False
        pass
    try:
        timer.resume()
        assert False
        pass
    except Exception:
        pass
    assert True
    return None
