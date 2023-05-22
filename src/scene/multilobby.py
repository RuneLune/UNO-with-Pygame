from overrides import overrides
from typing import List

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.multilobby.tablearea import TableArea
from gameobj.multilobby.userarea import UserArea
from gameobj.multilobby.playerarea import PlayerArea
from gameobj.multilobby.kickbtn import KickButton
from gameobj.multilobby.backbtn import BackButton
from gameobj.multilobby.dataproc import DataProcess
from client.client import SocketClient
from manager.gamemgr import GameManager


class MultiLobby(Scene):
    @overrides
    def start(self) -> None:
        self.socket_client: SocketClient = SocketClient()
        self.game_manager: GameManager = GameManager()

        table_area = TableArea()
        user_area = UserArea()

        self.instantiate(BackgroundObject(color.black))

        self.instantiate(table_area)
        self.instantiate(user_area)

        PlayerArea.destroy_all()
        KickButton.destroy_all()
        player_area_list: List[PlayerArea] = []
        for i in range(5):
            player_area = PlayerArea()
            player_area_list.append(player_area)
            self.instantiate(player_area)
            self.instantiate(
                KickButton().attach_player_area(player_area).attach_user_area(user_area)
            )
            continue

        data_process = DataProcess().attach_mgr(self.scene_manager)
        data_process.attach_user_area(user_area)
        data_process.attach_player_areas(player_area_list)
        self.instantiate(data_process)

        self.instantiate(BackButton("<Back").attach_mgr(self.scene_manager))

        result: bool = self.socket_client.initialize()
        if not result:
            self.scene_manager.load_previous_scene()
            return None
        self.socket_client.send_data(
            self.game_manager.username.strip(), "JOIN", self.socket_client.address
        )

        # data = None
        # while data is None:
        #     data = self.socket_client.poll_data()
        #     continue
        # room_info = data.target
        # user_area.nametxt = room_info["username"]
        # for i in range(len(room_info["player_list"])):
        #     player_area_list[i].nametxt = room_info["player_list"][i]
        #     if room_info["player_list"][i] == room_info["owner"]:
        #         player_area_list[i].nametxt += " (Owner)"
        #         pass
        #     continue

        return None
