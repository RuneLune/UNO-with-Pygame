from overrides import overrides
from typing import List

from ..gameobj import GameObject
from .userarea import UserArea
from .playerarea import PlayerArea
from client.client import SocketClient


class DataProcess(GameObject):
    @overrides
    def start(self) -> None:
        self.z_index = -9999
        self._socket_client: SocketClient = SocketClient()
        self._player_list = []
        self.invisible()
        return None

    @overrides
    def update(self) -> None:
        data_queue = self._socket_client.get_data()
        for data in data_queue:
            print(data)
            act = data.action
            if act == "INFO":
                self._user_area.nametxt = data.target["username"]
                if data.target["owner"] == data.target["username"]:
                    self._user_area.nametxt += " (Owner)"
                    pass
                self._player_list = data.target["player_list"]
                for i in range(len(data.target["player_list"])):
                    self._player_areas[i].nametxt = data.target["player_list"][i]
                    if data.target["player_list"][i] == data.target["owner"]:
                        self._player_areas[i].is_owner = True
                        pass
                    continue
                pass
            elif act == "OWNER":
                if data.player == self._user_area.nametxt:
                    self._user_area.is_owner = True
                pass
            elif act == "JOIN":
                self._player_list.append(data.player)
                self._player_areas[len(self._player_list) - 1].nametxt = data.player
                pass
            elif act == "DISCONNECT":
                self._player_list.remove(data.player)
                for i in range(len(self._player_areas)):
                    if i < len(self._player_list):
                        self._player_areas[i].nametxt = self._player_list[i]
                        pass
                    else:
                        self._player_areas[i].nametxt = ""
                        pass
                    continue
                pass
            continue
        return None

    def attach_user_area(self, user_area: UserArea) -> None:
        self._user_area = user_area
        return None

    def attach_player_areas(self, player_areas: List[PlayerArea]) -> None:
        self._player_areas = player_areas
        return None

    pass
