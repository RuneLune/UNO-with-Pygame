import pygame

from resource_manager import sound_resource
from settings_function import Settings


class SoundManager:
    def __init__(self, settings: Settings):
        self.settings = settings

        pygame.mixer.init()  # pygame.mixer 초기화
        self.background_sound = pygame.mixer.Sound(sound_resource("background.mp3"))
        self.deal_effect_sound = pygame.mixer.Sound(sound_resource("deal1.mp3"))
        self.discard_effect_sound = pygame.mixer.Sound(sound_resource("discard1.wav"))
        self.draw_effect_sound = pygame.mixer.Sound(sound_resource("draw1.wav"))
        self.shuffle_effect_sound = pygame.mixer.Sound(sound_resource("shuffle.mp3"))
        self.timeout_effect_sound = pygame.mixer.Sound(sound_resource("timeout.mp3"))
        self.click_effect_sound = pygame.mixer.Sound(sound_resource("click.mp3"))

        self.effect = {
            "deal": self.deal_effect_sound,
            "discard": self.discard_effect_sound,
            "draw": self.draw_effect_sound,
            "shuffle": self.shuffle_effect_sound,
            "timeout": self.timeout_effect_sound,
            "click": self.click_effect_sound,
        }

        self.is_background_playing = False

        self.refresh()

        return None

    def refresh(self) -> None:
        self.background_sound_volume = self.settings.get_settings().get(
            "background_sound_volume", 0.5
        )
        self.effect_sound_volume = self.settings.get_settings().get(
            "effect_sound_volume", 0.5
        )
        self.all_sound_volume = self.settings.get_settings().get(
            "all_sound_volume", 0.5
        )
        self.set_background_sound_volume()
        self.set_effect_sound_volume()

        return None

    def play_background_sound(self):
        if not self.is_background_playing:  # 배경음악이 재생중이 아니면
            self.background_sound.play(-1)  # 배경음악 재생
            self.is_background_playing = True  # 배경음악 재생중으로 표시

    def stop_background_sound(self):
        self.background_sound.stop()  # 배경음악 정지
        self.is_background_playing = False  # 배경음악 재생중이 아니라고 표시

    def set_background_sound_volume(self):
        self.background_sound.set_volume(
            self.background_sound_volume * self.all_sound_volume
        )  # 배경음악 음량 조절 0~1 사이값, 0은 음소거 1은 최대 볼륨

    def play_effect(self, name):
        if name in self.effect:
            self.effect[name].play()  # 효과음 재생

    def set_effect_sound_volume(self):
        for effect_sound in self.effect.values():
            effect_sound.set_volume(
                self.effect_sound_volume * self.all_sound_volume
            )  # 효과음 음량 조절 0~1 사이값, 0은 음소거 1은 최대 볼륨
