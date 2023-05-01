from __future__ import annotations

import pygame
from typing import List, Type, final


class GameObject(pygame.sprite.Sprite):
    """Abstract class for game objects"""

    # @final
    def __init__(
        self,
        surface: pygame.Surface,
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1.0,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._screen: pygame.Surface = pygame.display.get_surface()
        self._area: pygame.Rect = self._screen.get_rect()
        self._enabled: bool = True
        self._active: bool = True
        self._visible: bool = True
        self.tag: List[str] = []
        self.name: str = name
        self.z_index = z_index
        self.key_index = key_index
        self._mouse_over: bool = False
        self._clicked: bool = False
        if width < 0 or height < 0:
            self.image = surface
            self.rect = surface.get_rect()
            self.rect.left = left
            self.rect.top = top
            pass
        else:
            self.image = pygame.transform.scale(surface, (width, height))
            self.rect = pygame.Rect(left, top, width, height)
            pass
        self.reset()
        self.start()
        return None

    def reset(self) -> None:
        """reset to default values"""
        return None

    def start(self) -> None:
        """called on the frame when this object is enabled, before any of the update methods is called"""
        return None

    def update(self) -> None:
        """called every frame, if this object is enabled"""
        return None

    def awake(self) -> None:
        """called when this object is being loaded"""
        return None

    def on_became_invisible(self) -> None:
        """called when this object became invisible"""
        return None

    def on_became_visible(self) -> None:
        """called when this object became visible"""
        return None

    def on_destroy(self) -> None:
        """called when this object will be destroyed"""
        return None

    def on_enabled(self) -> None:
        """called when this object enabled and activated"""
        return None

    def on_mouse_down(self) -> None:
        """called when the user has pressed the mouse button while over this object"""
        return None

    def on_mouse_drag(self) -> None:
        """called when the user has clicked on this object and is still holding down the mouse"""
        return None

    def on_mouse_enter(self) -> None:
        """called when the mouse enters this object"""
        return None

    def on_mouse_exit(self) -> None:
        """called when the mouse is not any longer over this object"""
        return None

    def on_mouse_over(self) -> None:
        """called every frame while the mouse is over this object"""
        return None

    def on_mouse_up(self) -> None:
        """called when the user has released the mouse button"""
        return None

    def on_mouse_up_as_button(self) -> None:
        """only called when the mouse is released over the same object"""
        return None

    def on_key_down(self, key: int) -> bool:
        """called when the user has pressed the key"""
        return False

    def print(self) -> None:
        """logs message to console"""
        print(f"{type(self).__name__} {self.name}.print() called. ")
        return None

    # Methods under here should not be overrided

    @final
    def handle(self, event: Type[pygame.event.Event]) -> bool:
        """!DO NOT OVERRIDE! method for checking status"""
        if not self._active:
            return False
        if event.type == pygame.KEYDOWN:
            return self.on_key_down(event.key)
        if event.type == pygame.MOUSEMOTION:
            if self._clicked:
                self.on_mouse_drag()
                pass
            # self._check_mouse_over()
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self._mouse_over:
                self.on_mouse_down()
                self._clicked = True
                pass
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if self._clicked:
                self.on_mouse_up_as_button()
                self._clicked = False
                pass
            if self._mouse_over:
                self.on_mouse_up()
                pass
            pass
        return self._mouse_over

    @final
    def _check_mouse_over(self) -> None:
        """!DO NOT OVERRIDE! method for checking mouse collision"""
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position[0], mouse_position[1]):
            if not self._mouse_over:
                self.on_mouse_enter()
                pass
            self._mouse_over = True
            pass
        else:
            if self._mouse_over:
                self.on_mouse_exit()
                self._clicked = False
                pass
            self._mouse_over = False
            pass
        return None

    @final
    def tick(self) -> None:
        """!DO NOT OVERRIDE! method calls update() and render() method"""
        if not self._active:
            return None
        self._check_mouse_over()
        if self._mouse_over:
            self.on_mouse_over()
            pass
        self.update()
        if self._visible:
            self._render()
            pass
        return None

    @final
    def _render(self) -> None:
        """!DO NOT OVERRIDE! method renders this object"""
        self._screen.blit(self.image, self.rect)
        return None

    @final
    def __lt__(self, other: Type[GameObject]):
        return self.z_index < other.z_index

    pass
