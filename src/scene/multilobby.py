from overrides import overrides

import util.colors as color
from .scene import Scene
from gameobj.bgobj import BackgroundObject
from gameobj.multilobby.tablearea import TableArea
from gameobj.multilobby.handarea import HandArea
from gameobj.multilobby.playerarea import PlayerArea
from gameobj.multilobby.backbtn import BackButton


class MultiLobby(Scene):
    @overrides
    def start(self) -> None:
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

        return None
