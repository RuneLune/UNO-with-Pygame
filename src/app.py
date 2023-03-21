import pygame
import sys

from settings_function import Settings

from main_scene import main_scene
from start_scene import start_scene
from settings_scene import Settings_Scene

pygame.init()

settings = Settings()

screen = pygame.display.set_mode(settings.get_screen_resolution())

fps = 60
clock = pygame.time.Clock()
current_scene = "settings"

scenes = {
    "main": main_scene,
    "start": start_scene,
    "settings": Settings_Scene(settings),
}

pygame.display.set_caption("UNO with Pygame")

# Main loop
running = True
while running:
    scenes[current_scene].draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        else:
            res = scenes[current_scene].handle(event)

    if res[0] == "scene":
        scene = res[1]
        pygame.display.set_caption(res[1])

    # Update screen
    pygame.display.update()
    clock.tick(fps)

# Quit pygame
pygame.quit()
