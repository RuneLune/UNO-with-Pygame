import copy
import json
import os
from datetime import datetime
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
            self.reset()
            self.save()
        else:
            self.load()
        self.get_current_time(1)

        
    # Settings load method
    def load(self):
        # load saved settings from file
        if os.path.isfile(achieve_path):
            try:
                with open(achieve_path, "r") as f:
                    self.__achieve_states = json.load(f)
            except BaseException:
                # Error occurred while loading settings from file
                pass

    # Settings reset method
    def reset(self):
        global initial_settings
        self.__achieve_states = copy.deepcopy(initial_settings)

    # Settings save method
    def save(self):
        try:
            # Save settings to file
            with open(achieve_path, "w") as f:
                json.dump(self.__achieve_states, f)
        except BaseException:
            # Return -1 if an error occurred
            return -1

        self.load()
        # Return 0 if save was successful
        return 0

    def get_stage_states(self):
        return copy.deepcopy(self.__achieve_states)
    
    def get_current_time(self, idx):
        now = datetime.now()
        date_only = now.date()
        formatted_date = date_only.strftime("%Y.%m.%d")
        self.__achieve_states["date"][idx] = formatted_date
        self.save()
        pass

        return None
    