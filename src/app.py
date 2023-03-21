import pygame
import sys

from settings_function import Settings
import events

from main_scene import Main_Scene
from start_scene import Start_Scene
from settings_scene import Settings_Scene

pygame.init()

settings = Settings()

fps = 30
clock = pygame.time.Clock()
current_scene = "main"

scenes = {
    "main": Main_Scene(settings),
    "start": Start_Scene(settings),
    "settings": Settings_Scene(settings),
}

pygame.display.set_caption("Main Menu")

# Main loop
running = True
while running:
    scenes[current_scene].draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == events.CHANGE_SCENE:
            current_scene = event.target
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
