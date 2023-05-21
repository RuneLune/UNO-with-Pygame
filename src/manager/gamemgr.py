from __future__ import annotations

from typing import TYPE_CHECKING

from metaclass.singleton import SingletonMeta
from game.game import Game
from game.stage_a import StageA
from game.stage_b import StageB
from game.stage_c import StageC
from game.stage_d import StageD
from manager.lobbymgr import LobbyManager

if TYPE_CHECKING:
    from typing import Type, Dict, Callable


class GameManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.game_list: Dict[str, Callable[[int], Type[Game]]] = {
            "default": Game,
            "stage_a": StageA,
            "stage_b": StageB,
            "stage_c": StageC,
            "stage_d": StageD,
        }
        self.__current_game_type = "default"
        self.__players_count = LobbyManager().get_game_settings().get("player_count")
        self.__username = LobbyManager().get_game_settings().get("user_name")
        return None

    def create_game(self) -> None:
        self.__game: Type[Game] = self.game_list[self.__current_game_type](
            self.__players_count, self.__username
        )
        return None

    def create_stage(self, stage_type: str) -> None:
        self.__game = self.game_list[stage_type](username=self.__username)
        return None

    def get_game(self) -> Type[Game]:
        return self.__game

    @property
    def game_type(self) -> str:
        return self.__current_game_type

    @game_type.setter
    def game_type(self, game_type: str) -> None:
        self.__current_game_type = game_type
        return None

    @property
    def players(self) -> int:
        return self.__players_count

    @players.setter
    def players(self, players: int) -> None:
        self.__players_count = players
        return None

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username
        return None

    pass
