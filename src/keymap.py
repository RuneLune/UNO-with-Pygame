import pygame

key_saved = {
    "up": 1073741906,
    "down": 1073741905,
    "left": 1073741904,
    "right": 1073741903,
    "select": 13,
    "cancel": 27
}
key_default = {
    "up": 1073741906,
    "down": 1073741905,
    "left": 1073741904,
    "right": 1073741903,
    "select": 13,
    "cancel": 27
}  # default value is arrow, enter, escape


class KeyMap:
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.is_custom = False

    # if input is text, key is mapped
    def key_custom(self, target):
        pygame.event.wait()
        event = pygame.event.poll()
        if event.type == pygame.TEXTINPUT:
            key_saved[target] = pygame.key.key_code(event.text)
        elif event.type == pygame.KEYDOWN and key_default[target]:
            key_saved[target] = key_default[target]

    # return defalut key or user custom key
    def down(self):
        if self.is_custom is True:
            return self.keys[key_saved["down"]]
        else:
            return self.keys[pygame.K_DOWN]

    def up(self):
        if self.is_custom is True:
            return self.keys[key_saved["up"]]
        else:
            return self.keys[pygame.K_UP]

    def left(self):
        if self.is_custom is True:
            return self.keys[key_saved["left"]]
        else:
            return self.keys[pygame.K_LEFT]

    def right(self):
        if self.is_custom is True:
            return self.keys[key_saved["right"]]
        else:
            return self.keys[pygame.K_RIGHT]

    def select(self):
        if self.is_custom is True:
            return self.keys[key_saved["select"]]
        else:
            # pygame.K_RETURN is normal enter key
            return self.keys[pygame.K_RETURN]

    def cancel(self):
        if self.is_custom is True:
            return self.keys[key_saved["cancel"]]
        else:
            return self.keys[pygame.K_ESCAPE]

##########################
# key mapping test code

# pygame.init()
# win = pygame.display.set_mode((800, 600))
# clock = pygame.time.Clock()
# rect = pygame.Rect(0, 0, 40, 60)
# rect.center = win.get_rect().center
# vel = 50

# custom = True
# run = True
# while run:
#     clock.tick(10)

#     key_map = KeyMap()
#     key_map.is_custom = True

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#         if event.type == pygame.KEYDOWN and custom == True:
#             if pygame.key.name(event.key) == "up":
#                 key_map.key_custom("up")
#             elif pygame.key.name(event.key) == "down":
#                 key_map.key_custom("down")
#             elif pygame.key.name(event.key) == "left":
#                 key_map.key_custom("left")
#             elif pygame.key.name(event.key) == "right":
#                 key_map.key_custom("right")
#             elif pygame.key.name(event.key) == "enter":
#                 custom = False

#     rect.x += (key_map.right() - key_map.left()) * vel
#     rect.y += (key_map.down() - key_map.up()) * vel

#     win.fill((0, 0, 0))
#     pygame.draw.rect(win, (255, 0, 0), rect)
#     pygame.display.update()

# pygame.quit()
