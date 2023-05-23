from __future__ import annotations

import pygame
from typing import List, Type, final, Tuple
import copy


class GameObject(pygame.sprite.Sprite):
    """Abstract class for game objects"""

    # @final
    def __init__(
        self,
        surface: pygame.Surface = pygame.Surface((0, 0)),
        name: str = "GameObject",
        width: int = -1,
        height: int = -1,
        left: int = 0,
        top: int = 0,
        z_index: int = -1,
        key_index: int = -1.0,
        screen: pygame.Surface = None,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        if screen is None:
            self._screen: pygame.Surface = pygame.display.get_surface()
            pass
        else:
            self._screen: pygame.Surface = screen
            pass
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
        self._last_x_position: str = "left"
        self._last_y_position: str = "top"
        if width < 0 or height < 0:
            self.image = surface
            self.rect = surface.get_rect()
            self.rect.topleft = (left, top)
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

    def on_key_up(self, key: int) -> bool:
        """called when the user has released the key"""
        return False

    def on_text_edit(self, text: str) -> bool:
        """called when the user has edited the text"""
        return False

    def on_text_input(self, text: str) -> bool:
        """called when the user has inputted the text"""
        return False

    def print(self) -> None:
        """logs message to console"""
        print(f"{type(self).__name__} {self.name}.print() called. ")
        return None

    # Methods under here should not be overrided

    @property
    def width(self) -> int:
        """width of this object"""
        return self.rect.width

    @property
    def height(self) -> int:
        """height of this object"""
        return self.rect.height

    @property
    def left(self) -> int:
        """left position of this object"""
        return self.rect.left

    @property
    def top(self) -> int:
        """top position of this object"""
        return self.rect.top

    @property
    def right(self) -> int:
        """right position of this object"""
        return self.rect.right

    @property
    def bottom(self) -> int:
        """bottom position of this object"""
        return self.rect.bottom

    @property
    def center(self) -> int:
        """center position of this object"""
        return self.rect.center

    @property
    def centerx(self) -> int:
        """center x position of this object"""
        return self.rect.centerx

    @property
    def centery(self) -> int:
        """center y position of this object"""
        return self.rect.centery

    @property
    def topleft(self) -> Tuple[int, int]:
        """top left position of this object"""
        return self.rect.topleft

    @property
    def topright(self) -> Tuple[int, int]:
        """top right position of this object"""
        return self.rect.topright

    @property
    def bottomleft(self) -> Tuple[int, int]:
        """bottom left position of this object"""
        return self.rect.bottomleft

    @property
    def bottomright(self) -> Tuple[int, int]:
        """bottom right position of this object"""
        return self.rect.bottomright

    @property
    def midtop(self) -> Tuple[int, int]:
        """mid top position of this object"""
        return self.rect.midtop

    @property
    def midleft(self) -> Tuple[int, int]:
        """mid left position of this object"""
        return self.rect.midleft

    @property
    def midbottom(self) -> Tuple[int, int]:
        """mid bottom position of this object"""
        return self.rect.midbottom

    @property
    def midright(self) -> Tuple[int, int]:
        """mid right position of this object"""
        return self.rect.midright

    @property
    def size(self) -> Tuple[int, int]:
        """size of this object"""
        return self.rect.size

    @property
    def area(self) -> pygame.Rect:
        """area of this object"""
        return copy.deepcopy(self.rect)

    @width.setter
    def width(self, value: int) -> None:
        """width of this object"""
        self.rect.width = value
        return None

    @height.setter
    def height(self, value: int) -> None:
        """height of this object"""
        self.rect.height = value
        return None

    @left.setter
    def left(self, value: int) -> None:
        """left position of this object"""
        self.rect.left = value
        self._last_x_position
        return None

    @top.setter
    def top(self, value: int) -> None:
        """top position of this object"""
        self.rect.top = value
        self._last_y_position = "top"
        return None

    @right.setter
    def right(self, value: int) -> None:
        """right position of this object"""
        self.rect.right = value
        self._last_x_position = "right"
        return None

    @bottom.setter
    def bottom(self, value: int) -> None:
        """bottom position of this object"""
        self.rect.bottom = value
        self._last_y_position = "bottom"
        return None

    @center.setter
    def center(self, value: int) -> None:
        """center position of this object"""
        self.rect.center = value
        self._last_x_position = "center"
        self._last_y_position = "center"
        return None

    @centerx.setter
    def centerx(self, value: int) -> None:
        """center x position of this object"""
        self.rect.centerx = value
        self._last_x_position = "center"
        return None

    @centery.setter
    def centery(self, value: int) -> None:
        """center y position of this object"""
        self.rect.centery = value
        self._last_y_position = "center"
        return None

    @topleft.setter
    def topleft(self, value: Tuple[int, int]) -> None:
        """top left position of this object"""
        self.rect.topleft = value
        self._last_x_position = "left"
        self._last_y_position = "top"
        return None

    @topright.setter
    def topright(self, value: Tuple[int, int]) -> None:
        """top right position of this object"""
        self.rect.topright = value
        self._last_x_position = "right"
        self._last_y_position = "top"
        return None

    @bottomleft.setter
    def bottomleft(self, value: Tuple[int, int]) -> None:
        """bottom left position of this object"""
        self.rect.bottomleft = value
        self._last_x_position = "left"
        self._last_y_position = "bottom"
        return None

    @bottomright.setter
    def bottomright(self, value: Tuple[int, int]) -> None:
        """bottom right position of this object"""
        self.rect.bottomright = value
        self._last_x_position = "right"
        self._last_y_position = "bottom"
        return None

    @midtop.setter
    def midtop(self, value: Tuple[int, int]) -> None:
        """mid top position of this object"""
        self.rect.midtop = value
        self._last_x_position = "center"
        self._last_y_position = "top"
        return None

    @midleft.setter
    def midleft(self, value: Tuple[int, int]) -> None:
        """mid left position of this object"""
        self.rect.midleft = value
        self._last_x_position = "left"
        self._last_y_position = "center"
        return None

    @midbottom.setter
    def midbottom(self, value: Tuple[int, int]) -> None:
        """mid bottom position of this object"""
        self.rect.midbottom = value
        self._last_x_position = "center"
        self._last_y_position = "bottom"
        return None

    @midright.setter
    def midright(self, value: Tuple[int, int]) -> None:
        """mid right position of this object"""
        self.rect.midright = value
        self._last_x_position = "right"
        self._last_y_position = "center"
        return None

    @size.setter
    def size(self, value: Tuple[int, int]) -> None:
        """size of this object"""
        self.rect.size = value
        return None

    @area.setter
    def area(self, value: pygame.Rect) -> None:
        """area of this object"""
        self.rect = value
        return None

    @final
    def handle(
        self, event: Type[pygame.event.Event], mouse_overed: bool = False
    ) -> None:
        """!DO NOT OVERRIDE! method for checking status"""
        if not self._active:
            return False
        self.last_event = event
        if event.type == pygame.KEYDOWN:
            return self.on_key_down(event.key)
        elif event.type == pygame.KEYUP:
            return self.on_key_up(event.key)
        if not self._visible:
            return False
        # self._check_mouse_over(mouse_overed)
        if event.type == pygame.MOUSEMOTION:
            if self._clicked:
                self.on_mouse_drag()
                pass
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if self._clicked and self._mouse_over:
                self.on_mouse_up_as_button()
                pass
            if self._mouse_over:
                self.on_mouse_up()
                pass
            self._clicked = False
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self._mouse_over:
                self.on_mouse_down()
                self._clicked = True
                pass
            pass
        elif event.type == pygame.TEXTINPUT:
            self.on_text_input(event.text)
            pass
        elif event.type == pygame.TEXTEDITING:
            self.on_text_edit(event.text)
            pass

        return self._mouse_over

    @final
    def _check_mouse_over(self, mouse_overed: bool = False) -> None:
        """!DO NOT OVERRIDE! method for checking mouse collision"""
        mouse_position = pygame.mouse.get_pos()
        if (
            self.rect.collidepoint(mouse_position[0], mouse_position[1])
            and not mouse_overed
        ):
            self._check_mouse_enter()
            pass
        else:
            self._check_mouse_exit()
            pass
        return None

    @final
    def _check_mouse_enter(self) -> None:
        if not self._mouse_over:
            self.on_mouse_enter()
            pass
        self._mouse_over = True
        return None

    @final
    def _check_mouse_exit(self) -> None:
        if self._mouse_over:
            self.on_mouse_exit()
            pass
        self._mouse_over = False
        return None

    @final
    def tick(self, mouse_overed: bool = False) -> bool:
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
        return self._mouse_over

    @final
    def _render(self) -> None:
        """!DO NOT OVERRIDE! method renders this object"""
        self._screen.blit(self.image, self.rect)
        return None

    @final
    def __lt__(self, other: Type[GameObject]):
        return self.z_index < other.z_index

    def visible(self) -> None:
        self._visible = True
        self.on_became_visible()
        return None

    def invisible(self):
        self._visible = False
        self.on_became_invisible()
        return None

    def enable(self):
        self._active = True
        self.on_enabled()
        return None

    def disable(self):
        self._active = False
        return None

    # @property
    # def image(self) -> pygame.Surface:
    #     return self.image

    # @image.setter
    # def image(self, image: pygame.Surface) -> None:
    #     self.image = image
    #     coordinates = self.rect.topleft
    #     self.rect = self.image.get_rect()
    #     self.rect.topleft = coordinates
    #     return None

    # @property
    # def rect(self) -> pygame.Rect:
    #     return self.rect

    # @rect.setter
    # def rect(self, rect: pygame.Rect) -> None:
    #     self.rect = rect
    #     self.image = pygame.transform.scale(self.image, self.rect.size)
    #     return None

    pass
