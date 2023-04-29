from gameobj.gameobj import GameObject
from overrides import overrides
import pygame

# 게임에서 사용될 카드를 시작시 모두 로딩, not visible 상태
# 처음 분배된 카드는 순서에 맞춰서 유저와 봇 공간으로 이동
#  - 봇의 카드는 뒷면으로 로딩후, 가지고있는 수 만큼만 표시
#  - 유저의 카드는 순서를 나타내는 멤버변수를 가짐
#  - 유저 카드의 인덱스에 따른 위치를 game_scene에서 미리 정의한 뒤 해당하는 위치로 이동
#
# 드로우 더미에 있는 카드들은 드로우 될 순서에 따라 정렬되어 있는 상태이고 마우스 클릭시 맨 위 카드가 드로우 됨
#
# 카드를 드로우 하는 경우 드로우 더미 위치에서 해당하는 유저 카드 인덱스 위치로 이동
#  - 먼저 visible 상태로 바꾸기
#  - 기존의 카드들은 애니메이션 없이 이동
# 카드를 내는 경우 버린카드 더미 맨 위로 이동, visible
#
# 유저의 턴이 아닌 경우 모두 작동하지 않아야 함
#
# game_scene에서는 다음과 같은 정보를 계속 업데이트 해야함:
# 1. 유저 카드 숫자,색
# 2. 유저 카드들 각각의 인덱스(순서)


class Card(GameObject):
    @overrides
    def __init__(
        self,
        surface: pygame.Surface,
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
    ) -> None:
        super().__init__(surface, name, width, height, left, top, z_index)
        self.hands = False

    def on_mouse_enter(self) -> None:
        # 낼 수 있는 카드인 경우 리프트
        return super().on_mouse_enter()

    def on_mouse_exit(self) -> None:
        return super().on_mouse_exit()

    def on_mouse_over(self) -> None:
        return super().on_mouse_over()
