import pygame

from component.scene import Scene
from component.gameobj import GameObject


pygame.init()
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((800, 600))

scene = Scene()


class TestObject(GameObject):
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


test_surface1 = pygame.Surface((75, 100))
test_surface1.fill((255, 255, 255))
test_surface2 = pygame.Surface((75, 100))
test_surface2.fill((255, 255, 0))
test_surface3 = pygame.Surface((75, 100))
test_surface3.fill((255, 0, 255))
test_surface4 = pygame.Surface((75, 100))
test_surface4.fill((0, 255, 255))
test_surface5 = pygame.Surface((75, 100))
test_surface5.fill((0, 0, 255))
test_surface6 = pygame.Surface((75, 100))
test_surface6.fill((0, 255, 0))
test_surface7 = pygame.Surface((75, 100))
test_surface7.fill((255, 0, 0))
scene.create(TestObject(test_surface1, "Test Object 1", -1, -1, 25, 300, 1))
scene.create(TestObject(test_surface2, "Test Object 1", -1, -1, 125, 300, 2))
scene.create(TestObject(test_surface3, "Test Object 1", -1, -1, 225, 300, 3))
scene.create(TestObject(test_surface4, "Test Object 1", -1, -1, 325, 300, 4))
scene.create(TestObject(test_surface5, "Test Object 1", -1, -1, 425, 300, 5))
scene.create(TestObject(test_surface6, "Test Object 1", -1, -1, 525, 300, 6))
scene.create(TestObject(test_surface7, "Test Object 1", -1, -1, 625, 300, 7))


running: bool = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        scene.handle(event)
        continue
    scene.update()

    pygame.display.flip()
    clock.tick(fps)
    continue
