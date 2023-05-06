import pygame
from overrides import overrides
from os.path import join

import copy
import json
import os

import util.colors as colors
import event.events as events
from sound.sound import SoundManager
from util.resource_manager import font_resource, image_resource
from game.stage_a import Stage_A
from game.stage_b import Stage_B
from game.stage_c import Stage_C
from game.stage_d import Stage_D
from util.appdata_manager import stage_access_path


initial_settings = {"touchable": [True, True, False, False, False]}


class Stage():
    
    @overrides
    def handle(self, event: pygame.event.Event):
        if event.type == events.GAME_END:
            if (
                hasattr(event, "args")
                and "stage" in event.args
                and "status" in event.args
            ):
                if event.args.get("status") == "win":
                    if event.args.get("stage") == "stage_a":
                        self.__stage_states["touchable"][2] = True
                        self.save_stage_states()
                        pass
                    elif event.args.get("stage") == "stage_b":
                        self.__stage_states["touchable"][3] = True
                        self.save_stage_states()
                        pass
                    elif event.args.get("stage") == "stage_c":
                        self.__stage_states["touchable"][4] = True
                        self.save_stage_states()
                        pass
                    pass
                pass

            pass
        
