import pygame
import sys

import colors

pygame.init()

# Set up the screen
screen_size = (1280, 960)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Main Menu")

# Set menu options
menu_options = ["Start", "Settings", "Quit"]
menu_text = []
menu_rect = []

# Set up the font
title_font = pygame.font.SysFont("Arial", round(screen_size[1] / 3))
menu_font = pygame.font.SysFont(
    "Arial", round(screen_size[1] / (3.3 * len(menu_options)))
)

# Set title text
title_text = title_font.render("UNO", True, colors.black)
title_rect = title_text.get_rect()
title_rect.centerx = screen.get_rect().centerx
title_rect.bottom = screen.get_rect().centery

for i in range(len(menu_options)):
    menu_text.append(menu_font.render(menu_options[i], True, colors.black))
    menu_rect.append(menu_text[i].get_rect())
    menu_rect[i].centerx = screen.get_rect().centerx
    menu_rect[i].top = screen.get_rect().centery + i * screen_size[1] / (
        3 * len(menu_options)
    )

# Set selection rect
select_rect = pygame.Rect(
    0, 0, screen_size[0] / 3, screen_size[1] / (3 * len(menu_options))
)

selected_menu = 0


# Define menu function
def menu_func(i):
    if i == 0:  # Start
        return ("scene", "start")
    elif i == 1:  # Settings
        return ("scene", "settings")
    elif i == 2:  # Exit
        return ("exit", "none")
    else:
        print(menu_options[i] + " clicked")


def main_scene():
    global selected_menu
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(menu_options)):
                if menu_rect[i].collidepoint(mouse_pos):
                    selected_menu = i
                    continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(menu_options)):
                if menu_rect[i].collidepoint(mouse_pos):
                    return menu_func(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_menu -= 1
                if selected_menu < 0:
                    selected_menu = len(menu_options) - 1
            elif event.key == pygame.K_DOWN:
                selected_menu += 1
                if selected_menu >= len(menu_options):
                    selected_menu = 0
            elif event.key == pygame.K_RETURN:
                return menu_func(selected_menu)
    
    select_rect.center = menu_rect[selected_menu].center

    # Fill background
    screen.fill(colors.white)

    # Draw Title
    screen.blit(title_text, title_rect)

    # Draw select rect
    pygame.draw.rect(screen, colors.black, select_rect, 2)

    # Draw menu options
    for i in range(len(menu_text)):
        screen.blit(menu_text[i], menu_rect[i])

    return ("continue", "none")
