from game import Game
from overrides import overrides


class Stage_D(Game):
    @overrides
    def __init__(self) -> None:
        super(Stage_D, self).__init__(4)
        self._name = "stage_d"
        return None
