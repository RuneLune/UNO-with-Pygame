import pygame

# import sys

pygame.init()

# set up the screen
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("Main Menu")
fps = 60
clock = pygame.time.Clock()

# set up the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# set up the rectangle
rect_width = screen_width / 4
rect_height = rect_width / 4

# set up the font
title_font = pygame.font.SysFont("나눔고딕", round(screen_height / 3))
menu_font = pygame.font.SysFont("나눔고딕", round(rect_height * 0.8))

# set up the buttons
start_button = pygame.Rect(
    (screen_width - rect_width) / 2, screen_height / 2, rect_width, rect_height
)
settings_button = pygame.Rect(
    (screen_width - rect_width) / 2,
    screen_height / 2 + rect_height * 1.5,
    rect_width,
    rect_height,
)
quit_button = pygame.Rect(
    (screen_width - rect_width) / 2,
    screen_height / 2 + rect_height * 3,
    rect_width,
    rect_height,
)

# set up the button text
title_text = title_font.render("UNO", True, black)
start_text = menu_font.render("Start", True, black)
settings_text = menu_font.render("Settings", True, black)
quit_text = menu_font.render("Quit", True, black)

# game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # pygame.quit()
            # sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                print("Start button clicked")
            elif settings_button.collidepoint(mouse_pos):
                print("Settings button clicked")
            elif quit_button.collidepoint(mouse_pos):
                running = False

    # fill background
    screen.fill(white)

    # draw title text
    screen.blit(
        title_text,
        (
            screen_width / 2 - title_text.get_width() / 2,
            screen_height / 2 - title_text.get_height() * 1.2,
        ),
    )

    # draw buttons
    pygame.draw.rect(screen, green, start_button)
    pygame.draw.rect(screen, blue, settings_button)
    pygame.draw.rect(screen, red, quit_button)

    # draw button text
    screen.blit(
        start_text,
        (
            start_button.centerx - start_text.get_width() / 2,
            start_button.centery - start_text.get_height() / 2,
        ),
    )
    screen.blit(
        settings_text,
        (
            settings_button.centerx - settings_text.get_width() / 2,
            settings_button.centery - settings_text.get_height() / 2,
        ),
    )
    screen.blit(
        quit_text,
        (
            quit_button.centerx - quit_text.get_width() / 2,
            quit_button.centery - quit_text.get_height() / 2,
        ),
    )

    # update screen
    pygame.display.update()
    clock.tick(fps)

# quit pygame
pygame.quit()
