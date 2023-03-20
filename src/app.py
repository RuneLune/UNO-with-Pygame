import pygame
import sys

from settings_function import Settings

from main_scene import main_scene
from start_scene import start_scene
from settings_scene import Settings_Scene

pygame.init()

settings = Settings()

screen_size = settings.get_settings().get("screen_size", None)
screen = pygame.display.set_mode(screen_size)

fps = 60
clock = pygame.time.Clock()
current_scene = "settings"

scenes = {"main": main_scene, "start": start_scene, "settings": Settings_Scene(screen)}

pygame.display.set_caption("main")

# Main loop
running = True
while running:
    scenes[current_scene].draw()

    for event in pygame.event.get():
        scenes[current_scene].handle(event)

    # res = scenes[scene]()
    # if res[0] == "scene":
    #     scene = res[1]
    #     pygame.display.set_caption(res[1])
    # elif res[0] == "exit":
    #     pygame.quit()
    #     sys.exit()

    # Update screen
    pygame.display.update()
    clock.tick(fps)

# Quit pygame
pygame.quit()
