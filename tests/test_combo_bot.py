import os
import sys
import pygame

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from game.stage_a import StageA
import card.cards as cards

pygame.init()


def test_combo_bot() -> None:
    stage_a: StageA = StageA()
    stage_a.get_bots()[0].set_cards(
        [
            cards.blue_draw2,
            cards.green_draw2,
            cards.red_draw2,
            cards.yellow_draw2,
            cards.blue_0,
            cards.blue_1,
        ]
    )
    stage_a._bots[0].build_combo()
    if len(stage_a._bots[0]._max_combo) != 4:
        assert False
        pass
    else:
        assert True
        pass
    return None
