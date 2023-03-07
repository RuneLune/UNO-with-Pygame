import pygame
import sys
from pygame.locals import QUIT

# Variables
width = 600
height = 400
white = (255, 255, 255)
black = (0, 0, 0)
fps = 30

# Pygame initialize
pygame.init()

pygame.display.set_caption("Hello, world!")
displaysurf = pygame.display.set_mode((width, height), 0, 32)
clock = pygame.time.Clock()

gulimfont = pygame.font.SysFont("arial", 70)
helloworld = gulimfont.render("Hello, world!", 1, black)
hellorect = helloworld.get_rect()
hellorect.center = (width / 2, height / 2)

# Pygame main
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    displaysurf.fill(white)
    displaysurf.blit(helloworld, hellorect)

    pygame.display.update()
    clock.tick(fps)
