from gameobj.gameobj import GameObject


class Deck(GameObject):
    def on_mouse_over(self) -> None:
        # 하이라이팅
        return super().on_mouse_over()

    def on_mouse_down(self) -> None:
        # 카드 드로우
        return super().on_mouse_down()
