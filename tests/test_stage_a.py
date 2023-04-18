import os
import sys
from overrides import overrides

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src")
)

from stage_a import Stage_A
import cards


class Stage_A_test(Stage_A):
    @overrides
    def __init__(self) -> None:
        self._players = []
        self._force_draw = 0
        self._add_players()
        return None

    def check_computer_draw1(self) -> int:
        self._draw_pile = [cards.blue_0, cards.blue_draw2] * 50
        self._computer.set_cards([])
        self._deal_hands(1)
        return self._computer.get_hand_cards()[0]


def test_bot_drawing():
    stage_a_test: Stage_A_test = Stage_A_test()

    normal_count: int = 0
    functional_count: int = 0
    for i in range(50000):
        drawing_card: int = stage_a_test.check_computer_draw1()
        if cards.check_card(drawing_card).get("type") == "normal":
            normal_count += 1
            pass
        else:
            functional_count += 1
            pass
        continue
    target_ratio: float = 1.5
    result_ratio: float = functional_count / normal_count
    result_error: float = 100 - result_ratio / target_ratio * 100
    print("\n")
    print("target ratio: " + str(target_ratio))
    print(
        "result ratio: "
        + str(functional_count)
        + " / "
        + str(normal_count)
        + " = "
        + str(round(result_ratio, 4))
    )
    print("ratio error: " + str(round(result_error, 4)) + " %")
    if abs(result_error) > 5:
        assert False
        pass
    else:
        assert True
        pass
    pass
