from overrides import overrides
import pygame

from ..gameobj import GameObject
import util.colors as color


class Selector(GameObject):
    @overrides
    def start(self) -> None:
        screen_size = pygame.display.get_surface().get_size()
        self.image = pygame.Surface((screen_size[0] * 2 // 5, screen_size[1] // 11))
        self.image.fill(color.white)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color.black, self.rect, screen_size[0] // 256)
        self.z_index = -100
        return None

    pass
