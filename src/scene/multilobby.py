from overrides import overrides

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.multilobby.tablearea import TableArea
from gameobj.multilobby.handarea import HandArea
from gameobj.multilobby.playerarea import PlayerArea
from gameobj.multilobby.backbtn import BackButton
from client.client import SocketClient
from manager.gamemgr import GameManager


class MultiLobby(Scene):
    @overrides
    def start(self) -> None:
        self.socket_client: SocketClient = SocketClient()
        self.game_manager: GameManager = GameManager()

        table_area = TableArea()
        hand_area = HandArea()

        self.instantiate(BackgroundObject(color.black))

        self.instantiate(table_area)
        self.instantiate(hand_area)

        PlayerArea.destroy_all()
        player_area_list = []
        for i in range(5):
            player_area_list.append(PlayerArea())
            self.instantiate(player_area_list[-1])
            continue

        self.instantiate(BackButton("<Back").attach_mgr(self.scene_manager))

        result: bool = self.socket_client.initialize()
        if not result:
            self.scene_manager.load_previous_scene()
            return None
        self.socket_client.send_data(self.game_manager.username.strip(), "JOIN")

        return None
