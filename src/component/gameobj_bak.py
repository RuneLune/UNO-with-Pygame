from abc import ABC, abstractmethod


class GameObject:
    """Abstract class for game objects"""
    def __init__(self) -> None:
        self.start()
        return None

    def start() -> None:
        """Method called during initialize"""
        return None
    pass


class IDrawable(ABC):
    """Interface for drawable objects"""
    @abstractmethod
    def draw():
        """Method draws self on screen every tick"""
        raise NotImplementedError("Must override Drawable.draw()")
    pass


class IUpdatable(ABC):
    """Interface for updatable objects"""
    @abstractmethod
    def update():
        """Method updates self on each tick"""
        raise NotImplementedError("Must override Updatable.update()")
    pass


class UGameObject(GameObject, IUpdatable):
    """Abstract class for updatable game objects"""
    pass


class DGameObject(GameObject, IDrawable):
    """Abstract class for drawable game objects"""
    pass


class DUGameObject(UGameObject, DGameObject):
    """Abstract class for drawable and updatable game objects"""
    pass
