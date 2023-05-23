from overrides import overrides
from typing import Tuple
import pygame
from typing import Optional, TYPE_CHECKING, List

from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
import util.colors as colors


class BackToMain(TextButtonObject):
    def attach_mgr(self, scene_manager, target_scene: Optional[str] = None):
        self.scene_manager = scene_manager
        if target_scene is not None:
            self.target_scene = target_scene
            pass
        return self

    @overrides
    def on_click(self):
        self.scene_manager.load_scene(self.target_scene)
        return super().on_click()
