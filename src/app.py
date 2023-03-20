import pygame
import sys

from main_scene import main_scene
from start_scene import start_scene
from settings_scene import settings_scene

# pygame.init()

fps = 60
clock = pygame.time.Clock()
scene = "main"

scenes = {"main": main_scene, "start": start_scene, "settings": settings_scene}

pygame.display.set_caption("main")

# Main loop
running = True
while running:
    res = scenes[scene]()
    if res[0] == "scene":
        scene = res[1]
        pygame.display.set_caption(res[1])
    elif res[0] == "exit":
        pygame.quit()
        sys.exit()

    # Update screen
    pygame.display.update()
    clock.tick(fps)

# Quit pygame
pygame.quit()
