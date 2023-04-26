import pygame

from gameobj.gameobj import GameObject


class ColorCard(GameObject):
    def on_mouse_drag(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0] - self.mouse_gap[0]
        self.rect.y = mouse_pos[1] - self.mouse_gap[1]
        return None

    def on_mouse_down(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.prev_z_index = self.z_index
        self.z_index = 999
        self.mouse_gap = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        return None

    def on_mouse_up(self) -> None:
        self.z_index = self.prev_z_index
        self.mouse_gap = None
        return None

    def on_mouse_enter(self) -> None:
        self.rect_y_move += 1
        return None

    def on_mouse_exit(self) -> None:
        self.rect_y_move -= 1
        return None

    def start(self) -> None:
        self.rect_y_move = 0

    def update(self) -> None:
        if self.rect_y_move < 0:
            self.rect.move_ip(0, 5)
            self.rect_y_move += 1
            pass
        elif self.rect_y_move > 0:
            self.rect.move_ip(0, -5)
            self.rect_y_move -= 1
            pass
        return None

    pass
