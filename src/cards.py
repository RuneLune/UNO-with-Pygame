import math
import pygame


class Cards:
    def __new__(cls, *args, **kwargs):
        return super(Cards, cls).__new__(cls)

    def __init__(self, settings):
        self.__settings = settings
        self.__card_images = {}
        self.__render()
        return super(Cards, self).__init__()

    def refresh(self):
        self.__render()
        pass

    def __render(self):
        if self.__settings.get_settings().get("colorblind_mode") is False:
            image_directory = "res/img/default/"
        else:
            image_directory = "res/img/colorblind/"

        card_height = round(self.__settings.get_screen_resolution()[1] / 8)
        card_width = round(card_height * 409 / 585)

        card_code_list = (
            [0, 999]  # 카드 뒷면 및 ? 카드
            + list(range(wild_normal, wild_shuffle + 1))
            + list(range(blue_0, blue_skip + 1))
            + list(range(green_0, green_skip + 1))
            + list(range(red_0, red_skip + 1))
            + list(range(yellow_0, yellow_skip + 1))
        )

        for card_code in card_code_list:
            card_image = pygame.image.load(
                image_directory + str(card_code).zfill(3) + ".png"
            )
            self.__card_images.update(
                {
                    card_code: pygame.transform.scale(
                        card_image, (card_width, card_height)
                    )
                }
            )

    def get_card_image(self, card_code):
        return self.__card_images.get(card_code)


def check_card(card_code):
    color = math.floor(card_code / 100)
    if color == 1:
        color = "blue"
    elif color == 2:
        color = "green"
    elif color == 3:
        color = "red"
    elif color == 4:
        color = "yellow"
    else:
        color = "wild"

    type = "normal"
    number = card_code % 100
    if number == 10:
        type = "draw2"
    elif number == 11:
        type = "reverse"
    elif number == 12:
        type = "skip"
    elif number == 13:
        type = "normal"
    elif number == 14:
        type = "draw4"
    elif number == 15:
        type = "shuffle"
    elif number == 16:
        type = "custom"

    return {"color": color, "type": type, "number": number}


# Blue cards
blue_0 = 100
blue_1 = 101
blue_2 = 102
blue_3 = 103
blue_4 = 104
blue_5 = 105
blue_6 = 106
blue_7 = 107
blue_8 = 108
blue_9 = 109
blue_draw2 = 110
blue_reverse = 111
blue_skip = 112

# Green cards
green_0 = 200
green_1 = 201
green_2 = 202
green_3 = 203
green_4 = 204
green_5 = 205
green_6 = 206
green_7 = 207
green_8 = 208
green_9 = 209
green_draw2 = 210
green_reverse = 211
green_skip = 212

# Red cards
red_0 = 300
red_1 = 301
red_2 = 302
red_3 = 303
red_4 = 304
red_5 = 305
red_6 = 306
red_7 = 307
red_8 = 308
red_9 = 309
red_draw2 = 310
red_reverse = 311
red_skip = 312

# Yellow cards
yellow_0 = 400
yellow_1 = 401
yellow_2 = 402
yellow_3 = 403
yellow_4 = 404
yellow_5 = 405
yellow_6 = 406
yellow_7 = 407
yellow_8 = 408
yellow_9 = 409
yellow_draw2 = 410
yellow_reverse = 411
yellow_skip = 412

# Wild cards
wild_normal = 13
wild_draw4 = 14
wild_shuffle = 15
wild_custom = 16
