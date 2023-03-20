import pygame
import sys

import colors
from settings_function import Settings

pygame.init()

# Set up the screen
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Settings")

# Set menu options
menu_options = ["Back to main menu"]
menu_text = []
menu_rect = []

# Set up the font
# title_font = pygame.font.SysFont("Arial", round(screen_size[1] / 3))
title_font = pygame.font.SysFont("Arial", round(screen_size[1] / 10))
"""menu_font = pygame.font.SysFont(
    "Arial", round(screen_size[1] / (3.3 * len(menu_options)))
)"""
menu_font = pygame.font.SysFont("Arial", round(screen_size[1] / 10))

# Set title text
title_text = title_font.render("Settings Scene", True, colors.white)
title_rect = title_text.get_rect()
title_rect.centerx = screen.get_rect().centerx
title_rect.bottom = screen.get_rect().centery

for i in range(len(menu_options)):
    menu_text.append(menu_font.render(menu_options[i], True, colors.white))
    menu_rect.append(menu_text[i].get_rect())
    menu_rect[i].centerx = screen.get_rect().centerx
    menu_rect[i].top = screen.get_rect().centery + i * screen_size[1] / (
        3 * len(menu_options)
    )

settings = Settings()


# Define menu function
def menu_func(i):
    if i == 0:  # Back
        return ("scene", "main")
    else:
        print(menu_options[i] + " clicked")


def settings_scene():
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(menu_options)):
                if menu_rect[i].collidepoint(mouse_pos):
                    return menu_func(i)

    # Fill background
    screen.fill(colors.black)

    # Draw Title
    screen.blit(title_text, title_rect)

    # Draw menu options
    for i in range(len(menu_text)):
        screen.blit(menu_text[i], menu_rect[i])

    return "continue"
