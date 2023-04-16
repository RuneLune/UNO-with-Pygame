from abc import abstractmethod, ABC
import pygame


class Scene(ABC):
    def __new__(cls, *args, **kwargs):
        return super(Scene, cls).__new__(cls)

    def __init__(self):
        return super(Scene, self).__init__()

    @abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError("Must override refresh() method")

    @abstractmethod
    def handle(self, event: pygame.event.Event) -> None:
        raise NotImplementedError("Must override handle() method")

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError("Must override draw() method")
