import copy
import json
import os
from datetime import datetime
import pygame
import event.events as events

from util.appdata_manager import achieve_path

initial_settings = {"achieved": [False, False, False, False, False, False, False, False],
                    "date" : ["2019.01.21", "2019.01.21", "2019.01.21", "2019.01.21", "2019.01.21", "2019.01.21", "2019.01.21", "2019.01.21"],
                    "text": ["A: 싱글 플레이어 대전에서 승리", "B: 스토리 모드 클리어", "C: 싱글 게임에서 10턴 안에 승리", "D: 기술 카드 사용하지 않고 승리", "E: 다른 플레이어가 UNO 선언한 뒤 승리", "F: 모든 턴에서 5초 안에 카드 골라 승리", "G: 연속 3번 같은 숫자 내기", "H: 패에 빨간색 카드 모두 모으기"]}

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
    
    def update_achieve_state(self, idx):
        now = datetime.now()
        date_only = now.date()
        formatted_date = date_only.strftime("%Y.%m.%d")
        self.__achieve_states["achieved"][idx] = True
        self.__achieve_states["date"][idx] = formatted_date
        self.save()
        pass

        return None
    
    def get_achieve_text(self, idx):
        return self.__achieve_states["text"][idx]
    