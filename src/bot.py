from player import Player


class Bot(Player):
    def __new__(cls, *args, **kwargs):
        return super(Bot, cls).__new__(cls)

    def __init__(self, game, name):
        super(Bot, self).__init__(game, name)
