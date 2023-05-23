import copy
import json
import os
import pygame
import event.events as events
from metaclass.singleton import SingletonMeta

from util.appdata_manager import stage_access_path

initial_settings = {"touchable": [True, False, False, False]}


class StoryManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        global initial_settings
        self.__stage_states = initial_settings

        # Create settings.json if not exist
        if not os.path.isfile(stage_access_path):
            self.reset_stage_stages()
            self.save_stage_states()
        else:
            self.load_stage_states()

    # Settings load method
    def load_stage_states(self):
        # load saved settings from file
        if os.path.isfile(stage_access_path):
            try:
                with open(stage_access_path, "r") as f:
                    self.__stage_states = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass

    # Settings reset method
    def reset_stage_stages(self):
        global initial_settings
        self.__stage_states = copy.deepcopy(initial_settings)

    # Settings save method
    def save_stage_states(self):
        try:
            # Save settings to file
            with open(stage_access_path, "w") as f:
                json.dump(self.__stage_states, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load_stage_states()
        # Return 0 if save was successful
        return 0

    def get_stage_states(self):
        return copy.deepcopy(self.__stage_states)

    def handle(self, event: pygame.event.Event):
        if event.type == events.GAME_END:
            if (
                hasattr(event, "args")
                and "stage" in event.args
                and "status" in event.args
            ):
                if event.args.get("status") == "win":
                    if event.args.get("stage") == "stage_a":
                        self.__stage_states["touchable"][1] = True
                        self.save_stage_states()
                        pass
                    elif event.args.get("stage") == "stage_b":
                        self.__stage_states["touchable"][2] = True
                        self.save_stage_states()
                        pass
                    elif event.args.get("stage") == "stage_c":
                        self.__stage_states["touchable"][3] = True
                        self.save_stage_states()
                        pass
                    pass
                pass

    def update_stage_state(self, stage_name: str, status: bool):
        if status:
            if stage_name == "stage_a":
                self.__stage_states["touchable"][1] = 1
                self.save_stage_states()
                pass
            elif stage_name == "stage_b":
                self.__stage_states["touchable"][2] = 1
                self.save_stage_states()
                pass
            elif stage_name == "stage_c":
                self.__stage_states["touchable"][3] = 1
                self.save_stage_states()
                pass
        pass

        return None
