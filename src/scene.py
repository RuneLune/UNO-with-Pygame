from abc import abstractmethod, ABC
from typing import Dict
import pygame


class Scene(ABC):
    def __new__(cls, *args, **kwargs):
        return super(Scene, cls).__new__(cls)

    def __init__(self) -> None:
        return super(Scene, self).__init__()

    @abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError("Must override refresh() method")

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError("Must override render() method")

    @abstractmethod
    def handle(self, event: pygame.event.Event) -> None:
        raise NotImplementedError("Must override handle() method")

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError("Must override draw() method")

    # @abstractmethod
    # def get_args(self, args: Dict[any, any]) -> None:
    #     raise NotImplementedError("Must override draw() method")
