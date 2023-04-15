import pygame
import sys
from typing import Dict

from settings_function import Settings
import events

# from game_scene import Game_Scene
from main_scene import Main_Scene
from settings_scene import Settings_Scene
from gameUI import Game_UI
from game_lobby import Game_Lobby
from stage_select import Stage

pygame.init()

settings: Settings = Settings()

fps: int = 30
clock: pygame.time.Clock = pygame.time.Clock()
current_scene: str = "main"

scenes: Dict[str, Main_Scene | Game_Lobby | Settings_Scene | Game_UI] = {
    "main": Main_Scene(settings),
    "gamelobby": Game_Lobby(settings),
    "settings": Settings_Scene(settings),
    "gameui": Game_UI(settings),
    "stage": Stage(settings)
}

pygame.display.set_caption("Main Menu")

# Main loop
running: bool = True
while running:
    scenes[current_scene].draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == events.CHANGE_SCENE:
            current_scene = event.target
            if event.target == "gameui":
                scenes[current_scene].refresh(5)
            else:
                scenes[current_scene].refresh()
            continue
        else:
            res = scenes[current_scene].handle(event)

    # Update screen
    pygame.display.update()
    clock.tick(fps)

# Quit pygame
pygame.quit()
sys.exit()