import pygame

pygame.init()
win = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
rect = pygame.Rect(0, 0, 40, 60)
rect.center = win.get_rect().center
vel = 50

key = {"up": 1, "down": 1, "left": 0, "right": 0}


class KeyMap():
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.is_custom = False

    def key_custom_up(self):
        print(1)
        pygame.event.wait(5000)
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.TEXTINPUT:
                print(2)
                key["up"] = pygame.key.key_code(event.text)
            else:
                print(3)

    def key_custom_down(self):
        print(1)
        pygame.event.wait(5000)
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.TEXTINPUT:
                print(2)
                key["down"] = pygame.key.key_code(event.text)
            else:
                print(3)

    def key_custom_left(self):
        if pygame.event.type == pygame.KEYDOWN:
            key["left"] = pygame.key.key_code(pygame.event.key)

    def key_custom_right(self):
        if pygame.event.type == pygame.KEYDOWN:
            key["right"] = pygame.key.key_code(pygame.event.key)

    def left(self):
        if self.is_custom == True:
            return self.keys[key["left"]]
        else:
            return self.keys[pygame.K_LEFT]

    def right(self):
        if self.is_custom == True:
            return self.keys[key["right"]]
        else:
            return self.keys[pygame.K_RIGHT]

    def down(self):
        if self.is_custom == True:
            print(chr(key["down"]))
            return self.keys[pygame.key.key_code(chr(key["down"]))]
        else:
            print(self.keys[pygame.K_DOWN])
            return self.keys[pygame.key.key_code("down")]

    def up(self):
        if self.is_custom == True:
            return self.keys[pygame.key.key_code(chr(key["up"]))]
        else:
            return self.keys[pygame.key.key_code("up")]


run = True
custom = True

while run:
    clock.tick(3)

    key_map = KeyMap()
    key_map.is_custom = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if custom == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_map.key_custom_up()
                elif event.key == pygame.K_DOWN:
                    key_map.key_custom_down()
                    custom = False

    print("key:", key)

    rect.x += (key_map.right() - key_map.left()) * vel
    rect.y += (key_map.down() - key_map.up()) * vel

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), rect)
    pygame.display.update()

pygame.quit()
