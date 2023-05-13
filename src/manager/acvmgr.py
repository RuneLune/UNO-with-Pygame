import copy
import json
import os
import pygame
import event.events as events

from util.appdata_manager import achieve_path

initial_settings = {"achieved": [False, False, False, False, False, False, False, False],
                    "date" : ["2022.05.13", "2022.05.13", "2022.05.13", "2022.05.13", "2022.05.13", "2022.05.13", "2022.05.13", "2022.05.13"]}

class AchieveManager:
    def __init__(self) -> None:
        
        global initial_settings
        self.__achieve_states = initial_settings

        # Create settings.json if not exist
        if not os.path.isfile(achieve_path):
            self.reset_stage_stages()
            self.save_stage_states()
        else:
            self.load_stage_states()

        
    # Settings load method
    def load_stage_states(self):
        # load saved settings from file
        if os.path.isfile(achieve_path):
            try:
                with open(achieve_path, "r") as f:
                    self.__achieve_states = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass

    # Settings reset method
    def reset_stage_stages(self):
        global initial_settings
        self.__achieve_states = copy.deepcopy(initial_settings)

    # Settings save method
    def save_stage_states(self):
        try:
            # Save settings to file
            with open(achieve_path, "w") as f:
                json.dump(self.__achieve_states, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load_stage_states()
        # Return 0 if save was successful
        return 0

    def get_stage_states(self):
        return copy.deepcopy(self.__achieve_states)
    
    

        return None
    