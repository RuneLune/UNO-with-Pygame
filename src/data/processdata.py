from typing import Optional


class ProcessData:
    def __init__(self, player: str, action: str, target: Optional[str] = None):
        self.player = player
        self.action = action
        self.target = target
        return None

    def __str__(self):
        if self.target is None:
            return f"{self.player}:{self.action}"
        else:
            return f"{self.player}:{self.action}:{self.target}"
        pass

    pass
