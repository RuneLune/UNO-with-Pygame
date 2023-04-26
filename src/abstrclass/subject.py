from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .observer import Observer


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Type[Observer]) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Type[Observer]) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass
