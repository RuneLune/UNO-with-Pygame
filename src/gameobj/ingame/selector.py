from overrides import overrides
import pygame

from card.cards import Cards
from ..gameobj import GameObject
import util.colors as color
from gameobj.ingame.deck import Deck


class Selector(GameObject):
    @overrides
    def start(self) -> None:
        card_size = Cards().get_card_image(000).get_rect().size
        self.image = pygame.Surface(card_size, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color.white, self.rect, 5)
        self.image = Deck(pygame.Surface((0, 0))).create_neon(self.image)
        self.z_index = 1
        return None

    pass
