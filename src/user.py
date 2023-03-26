from player import Player


class User(Player):
    def __new__(cls, *args, **kwargs):
        return super(User, cls).__new__(cls)

    def __init__(self, game, name):
        super(User, self).__init__(game, name)
